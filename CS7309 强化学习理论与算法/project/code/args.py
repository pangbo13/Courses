import argparse
import re
import warnings

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', type=str, required=True)
    parser.add_argument('--replay_buffer_capacity', type=int, default=10000)
    parser.add_argument('--train_batch_size', type=int, default=128)
    parser.add_argument('--episode_limit', type=int, default=10000, help='maximum episode for training')
    parser.add_argument('--render', action='store_true', help='render environment')
    parser.add_argument('--gamma', type=float, default=0.98, help='discount factor')
    parser.add_argument('--force_run', choices=['value-base', 'value-base-cv', 'policy-base'], help='force run method, ignore check of environment, choose from value-base, value-base-cv, policy-base')

    vb_group = parser.add_argument_group(title='Value-base', description='For value-based method (Rainbow)')
    vb_group.add_argument('--target_dqn', action='store_true', help='use target DQN')
    vb_group.add_argument('--disable_noisy', action='store_true', help='disable noisy net')
    vb_group.add_argument('--disable_double_dqn', action='store_true', help='disable double DQN')
    vb_group.add_argument('--disable_priority', action='store_true', help='disable priority replay buffer')
    vb_group.add_argument('--disable_dueling', action='store_true', help='disable dueling DQN')
    vb_group.add_argument('--multi_step', type=int, default=3, help='multi-step for n-step DQN, set to 1 for vanilla DQN')

    vb_group.add_argument('--target_update_delay', type=int, default=2, help='delay for updating target network or exchanging double network')
    vb_group.add_argument('--learning_rate', type=float, default=0.001, help='learning rate')
    vb_group.add_argument('--test_delay', type=int, default=10, help='delay for testing')

    vb_group.add_argument('--init_epsilon', type=float, default=1, help='initial epsilon value for epsilon-greedy exploration')
    vb_group.add_argument('--min_epsilon', type=float, default=0.1, help='minimum epsilon value for epsilon-greedy exploration')
    vb_group.add_argument('--epsilon_decay', type=float, default=0.002, help='epsilon decay rate for epsilon-greedy exploration')

    pb_group = parser.add_argument_group(title='Policy-base', description='For policy-based method (DDPG)')
    pb_group.add_argument('--tau', type=float, default=0.005, help='soft update parameter')
    pb_group.add_argument('--sigma', type=float, default=0.01, help='noise parameter')
    pb_group.add_argument('--actor_lr', type=float, default=3e-4, help='actor learning rate')
    pb_group.add_argument('--critic_lr', type=float, default=3e-3, help='critic learning rate')

    return parser.parse_args()

def get_method_and_kwargs():
    args = get_args()
    SUPPORTED_ENV = {
        'VideoPinball-ramNoFrameskip': ['v4','value-base'],
        'Breakout-ramNoFrameskip': ['v4','value-base'],
        'Pong-ramNoFrameskip': ['v4','value-base'],
        'BreakoutNoFrameskip': ['v4','value-base-cv'],
        'HalfCheetah': ['v4','policy-base'],
        'Hopper': ['v4','policy-base'],
        'Ant': ['v4','policy-base'],
        'Humanoid': ['v4','policy-base'],
    }
    env_name = args.env_name.strip()
    if args.force_run:
        method = args.force_run
        full_env_name = env_name
        print('You are using force run mode, this will ignore check of environment')
        print('If you are not sure about this, please remove --force_run option')
        if input('Force run {} on {}? (y/[n])'.format(method, full_env_name)).lower() == 'y':
            print('** Force run {} on {}'.format(method, full_env_name))
            print('** Ignore check of environment')
        else:
            raise ValueError('Force run aborted')
    else:
        match = re.match(r'(.+)-(v\d)', env_name)
        if match:
            env_name, version = match.groups()
            if env_name not in SUPPORTED_ENV:
                raise ValueError('Unsupported environment: {}'.format(env_name))
            if version != SUPPORTED_ENV[env_name][0]:
                raise ValueError('Unsupported version: {}, expected: {}'.format(version, SUPPORTED_ENV[env_name][0]))
            method = SUPPORTED_ENV[env_name][1]
            full_env_name = '{}-{}'.format(env_name, SUPPORTED_ENV[env_name][0])
        else:
            if env_name not in SUPPORTED_ENV:
                raise ValueError('Unsupported environment: {}'.format(env_name))
            else:
                warnings.warn('No environment version specified, using default version: {}'.format(SUPPORTED_ENV[env_name][0]), stacklevel=2)
                method = SUPPORTED_ENV[env_name][1]
                full_env_name = '{}-{}'.format(env_name, SUPPORTED_ENV[env_name][0])
    print('Environment: {}'.format(full_env_name))
    if method == 'value-base' or method == 'value-base-cv':
        if args.target_dqn and not args.disable_double_dqn:
            raise ValueError('Can not use both target DQN and double DQN')
        main_kwargs = {
            'env_name': full_env_name,
            'replay_buffer_capacity': args.replay_buffer_capacity,
            'train_batch_size': args.train_batch_size,
            'episode_limit': args.episode_limit,
            'render': args.render,
            'target_dqn': args.target_dqn,
            'noisy': not args.disable_noisy,
            'double_dqn': not args.disable_double_dqn,
            'priority': not args.disable_priority,
            'dueling': not args.disable_dueling,
            'multi_step': args.multi_step,
            'gamma': args.gamma,
            'target_update_delay': args.target_update_delay,
            'learning_rate': args.learning_rate,
            'test_delay': args.test_delay,
            'init_epsilon': args.init_epsilon,
            'min_epsilon': args.min_epsilon,
            'epsilon_decay': args.epsilon_decay,
        }
    elif method == 'policy-base':
        main_kwargs = {
            'env_name': full_env_name,
            'replay_buffer_capacity': args.replay_buffer_capacity,
            'train_batch_size': args.train_batch_size,
            'episode_limit': args.episode_limit,
            'render': args.render,
            'tau': args.tau,
            'sigma': args.sigma,
            'actor_lr': args.actor_lr,
            'critic_lr': args.critic_lr,
            'gamma': args.gamma,
        }

    return method, full_env_name, main_kwargs

if __name__ == '__main__':
    print(get_method_and_kwargs())
