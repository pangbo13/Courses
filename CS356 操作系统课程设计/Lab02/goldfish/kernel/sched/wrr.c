/*
 * WRR Scheduling Class
 */

#include "sched.h"

#include <linux/slab.h>

static inline struct task_struct *wrr_task_of(struct sched_wrr_entity *wrr_se)
{
	return container_of(wrr_se, struct task_struct, wrr);
}

static inline int on_wrr_rq(struct sched_wrr_entity *wrr_se)
{
	return !list_empty(&wrr_se->run_list);
}
static inline struct wrr_rq *wrr_rq_of_se(struct sched_wrr_entity *wrr_se)
{
	struct task_struct *p = wrr_task_of(wrr_se);
	struct rq *rq = task_rq(p);

	return &rq->wrr;
}

static unsigned int get_rr_interval_wrr(struct rq *rq, struct task_struct *p);

/*
 * Update the current task's runtime statistics. Skip current tasks that
 * are not in our scheduling class.
 */
static void update_curr_wrr(struct rq *rq)
{
	struct task_struct *curr = rq->curr;
	struct sched_wrr_entity *wrr_se = &curr->wrr;
	struct wrr_rq *wrr_rq = wrr_rq_of_se(wrr_se);
	u64 delta_exec;

	if (curr->sched_class != &wrr_sched_class)
		return;

	delta_exec = rq->clock_task - curr->se.exec_start;
	if (unlikely((s64)delta_exec < 0))
		delta_exec = 0;

	schedstat_set(curr->se.statistics.exec_max,
			  max(curr->se.statistics.exec_max, delta_exec));

	curr->se.sum_exec_runtime += delta_exec;
	account_group_exec_runtime(curr, delta_exec);

	curr->se.exec_start = rq->clock_task;
	cpuacct_charge(curr, delta_exec);

	wrr_rq->wrr_time += delta_exec;

	printk("[WRR]update_curr_wrr: wrr_time:%llu\n",rq->wrr.wrr_time);
	if (rq->wrr.wrr_time >= global_wrr_runtime()){
		printk("[WRR]update_curr_wrr: resched %d\n",curr->pid);
		resched_task(curr);
	}
}


/*
 * Adding/removing a task to/from ready queue
 */
static void enqueue_task_wrr(struct rq *rq, struct task_struct *p, int flags)
{
	printk("[WRR]enqueue_task_wrr ");
	struct sched_wrr_entity *wrr_se = &p->wrr;
	int head = flags & ENQUEUE_HEAD;
	char* group_path;
	group_path = task_group_path(p->sched_task_group);

	//check whether new task in foreground and set its time slice
	if(group_path[1]=='\0'){	// foreground 
		wrr_se->time_slice = WRR_FORE_TIMESLICE;
		printk("pid:%d foreground\n",p->pid);
		p->wrr.weight = 10;
	}else{
		wrr_se->time_slice = WRR_BACK_TIMESLICE;
		printk("pid:%d background\n",p->pid);
		p->wrr.weight = 1;
	}

	if(head)
		list_add(&wrr_se->run_list, &(rq->wrr.run_list));
	else
		list_add_tail(&wrr_se->run_list, &(rq->wrr.run_list));
	
	++rq->wrr.wrr_nr_running;
	inc_nr_running(rq);
}

static void dequeue_task_wrr(struct rq *rq, struct task_struct *p, int flags){
	struct sched_wrr_entity *wrr_se = &p->wrr;

	update_curr_wrr(rq);

	if(rq->wrr.wrr_nr_running<=0||!on_wrr_rq(wrr_se))	//if nothing in rq or p not in rq, just return
		return;
	list_del_init(&wrr_se->run_list);
	--rq->wrr.wrr_nr_running;
	dec_nr_running(rq);
}

/*
 * Put task to the head or the tail of the run list without the overhead of
 * dequeue followed by enqueue.
 */
static void 
requeue_task_wrr(struct rq *rq, struct task_struct *p, int head)
{
	printk("[WRR]requeue_task_wrr: requeue pid:%d\n", p->pid);
	struct sched_wrr_entity *wrr_se = &p->wrr;
	struct list_head *queue = &(rq->wrr.run_list);
	if(!on_wrr_rq(wrr_se))
		return;

	if (head)
		list_move(&wrr_se->run_list, queue);
	else
		list_move_tail(&wrr_se->run_list, queue);
}

/*
 * Move task to the tail of rq.
 */
static void yield_task_wrr(struct rq *rq)
{
	requeue_task_wrr(rq, rq->curr, 0);
}

static void 
check_preempt_curr_wrr(struct rq *rq, struct task_struct *p, int flags)
{
	//switch to p if p as higher prio
	if (p->prio < rq->curr->prio) {
		resched_task(rq->curr);
		return;
	}
}

/*
* This function is used to select the next task to run. 
* If there is no ready task or the current round of WRR 
* has reached the time limit, it returns a NULL pointer.
*/
static struct task_struct *pick_next_task_wrr(struct rq *rq)
{
	struct sched_wrr_entity *wrr_se;
	struct task_struct *p;

	if (rq->wrr.wrr_nr_running == 0)
		{	//no task is waiting for time
			rq->wrr.wrr_time = 0;
			return NULL;
		}

	if (rq->wrr.wrr_time >= global_wrr_runtime()){
		//WRR running time of this round has reached the limit
		printk("[WRR]pick_next_task_wrr: time for wrr used up!\n");
		rq->wrr.wrr_time = 0;
		return NULL;
	}
		
	//get the first element in rq
	wrr_se = list_first_entry(&(rq->wrr.run_list), struct sched_wrr_entity, run_list);

	p = wrr_task_of(wrr_se);
	p->se.exec_start = rq->clock_task;

	printk("[WRR]pick_next_task_wrr: pick %d\n",p->pid);

	return p;
}

static void put_prev_task_wrr(struct rq *rq, struct task_struct *prev){
	printk("[WRR]put_prev_task_wrr\n");
	update_curr_wrr(rq);
	if(on_wrr_rq(&prev->wrr)){
		requeue_task_wrr(rq, prev, 0);						//move p to tail of rq
	}
}


#ifdef CONFIG_SMP	//we dont support SMP, so just ignore
static int select_task_rq_wrr(struct task_struct *p, int sd_flag, int flags)
{

}
static void set_cpus_allowed_wrr(struct task_struct *p,
				const struct cpumask *new_mask)
{

}
/* Assumes rq->lock is held */
static void rq_online_wrr(struct rq *rq)
{

}
/* Assumes rq->lock is held */
static void rq_offline_wrr(struct rq *rq)
{

}
static void pre_schedule_wrr(struct rq *rq, struct task_struct *prev)
{

}
static void post_schedule_wrr(struct rq *rq)
{

}
static void task_woken_wrr(struct rq *rq, struct task_struct *p)
{
}
static void switched_from_wrr(struct rq *rq, struct task_struct *p)
{

}
#endif

static void set_curr_task_wrr(struct rq *rq){
	struct task_struct *p = rq->curr;
	//set the execution start time
	p->se.exec_start = rq->clock_task;

}

/*
 * This function is invoked every 1ms,
 * and will update the remaining time slice of the task.
 * When it finds that the task time slice is exhausted, it will recalculate 
 * the time slice and mark the task as needing rescheduling.
*/
static void task_tick_wrr(struct rq *rq, struct task_struct *p, int queued){
	struct sched_wrr_entity *wrr_se = &p->wrr;
	update_curr_wrr(rq);
	printk("[WRR]task_tick_wrr:%d time_slice left:%d\n",p->pid,wrr_se->time_slice-1);
	//if time slice is not used up, just return
	if(--wrr_se->time_slice) return;
	//get new time slice
	wrr_se->time_slice = get_rr_interval_wrr(rq,p);
	//if p is the only task running on WRR, no need to switch
	if(!list_is_last(&(wrr_se->run_list),&(rq->wrr.run_list))){	
		printk("[WRR]task_tick_wrr: resched %d\n",p->pid);
		resched_task(p);
		// requeue_task_wrr(rq, p, 0);						//move p to tail of rq
	}
}

/*
* This function calculates the time slice and weight by the group to which the task belongs
*/
static unsigned int get_rr_interval_wrr(struct rq *rq, struct task_struct *p){
	char* group_path;
	group_path = task_group_path(p->sched_task_group);
	printk("[WRR]get_rr_interval_wrr:");
	if(group_path[1]=='\0'){	// foreground 
		printk("pid:%d foreground\n",p->pid);
		p->wrr.weight = 10;
		return WRR_FORE_TIMESLICE;
	}else{
		printk("pid:%d background\n",p->pid);
		p->wrr.weight = 1;
		return WRR_BACK_TIMESLICE;
	}
}

/*
* This function is invoked when the prio of a task is changed,
* we ignore this function because we already grouped tasks into
* background and foreground.
*/
static void prio_changed_wrr(struct rq *rq, struct task_struct *p, int oldprio)
{

}

/*
 * This function is invoked when switching a task to WRR.
 * We could just ignore this function. 
 */
static void switched_to_wrr(struct rq *rq, struct task_struct *p){

}

void init_wrr_rq(struct wrr_rq *wrr_rq, struct rq *rq)
{
	INIT_LIST_HEAD(&wrr_rq->run_list);
	wrr_rq->wrr_nr_running = 0;
	wrr_rq->wrr_time = 0;
	#ifdef CONFIG_WRR_GROUP_SCHED
	wrr_rq->rq = rq;
	#endif
}
const struct sched_class wrr_sched_class = {
	.next			= &fair_sched_class, //Required
	.enqueue_task		= enqueue_task_wrr, //Required
	.dequeue_task		= dequeue_task_wrr, //Required
	.yield_task		= yield_task_wrr, //Required

	.check_preempt_curr	= check_preempt_curr_wrr, //Required

	.pick_next_task		= pick_next_task_wrr, //Required
	.put_prev_task		= put_prev_task_wrr, //Required

#ifdef CONFIG_SMP
	.select_task_rq		= select_task_rq_wrr,

	.set_cpus_allowed       = set_cpus_allowed_wrr,
	.rq_online              = rq_online_wrr,
	.rq_offline             = rq_offline_wrr,
	.pre_schedule		= pre_schedule_wrr,
	.post_schedule		= post_schedule_wrr,
	.task_woken		= task_woken_wrr,
	.switched_from		= switched_from_wrr,
#endif

	.set_curr_task          = set_curr_task_wrr, //Required
	.task_tick		= task_tick_wrr, //Required

	.get_rr_interval	= get_rr_interval_wrr, //Required

	.prio_changed		= prio_changed_wrr,
	.switched_to		= switched_to_wrr,
};