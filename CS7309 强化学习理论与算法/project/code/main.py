import args

if __name__ == '__main__':
    method, full_env_name, main_kwargs = args.get_method_and_kwargs()
    
    try:
        import gymnasium
    except ImportError:
        raise ImportError('Cannot import gymnasium')
    else:
        print('Current gymnasium version: {}'.format(gymnasium.__version__))
        if gymnasium.__version__ != '0.29.1':
            print('gymnasium version is not 0.29.1, you may encounter some problems')
    try:
        import torch
    except ImportError:
        raise ImportError('Cannot import torch')
    else:
        print('Current torch version: {}'.format(torch.__version__))
        if torch.cuda.is_available():
            print('Current cuda version: {}'.format(torch.version.cuda))
        else:
            print('CUDA is not available')

    for k, v in main_kwargs.items():
        print('{:>20}: {}'.format(k, v))
    if method == 'value-base':
        print('Using value-based method to solve the environment')
        print('Loading rainbow_v5.py')
        from rainbow_v5 import main
        main(**main_kwargs)
    elif method == 'value-base-cv':
        print('Using value-based method to solve the environment')
        print('Loading rainbow_v1_cv.py')
        from rainbow_cv_v1 import main
        main(**main_kwargs)
    elif method == 'policy-base':
        print('Using policy-based method to solve the environment')
        print('Loading ddpg_v2.py')
        from ddpg_v2 import main
        main(**main_kwargs)