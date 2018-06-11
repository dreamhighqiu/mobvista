HOST = ['192.168.1.185', ]
DICT_LOG = {
    "1": {
        "log_name": "adn_net",
        "root_path": '/data/adn_logs/stat_v3/',
        "log_path": '/data/adn_logs/stat_v3/{log_type}/{cur_month}/{cur_date}/{cur_hour}.log',
        "log_params_path": "data/adnnet_params.config"
    },
    "2": {
        "log_name": "midway_server",
        "root_path": '/data/adn_logs/midway/',
        "log_path": '/data/adn_logs/midway/{log_type}/{log_type}.log.{cur_hour}',
        "log_params_path": "data/midway_params.config"
    },
    "3": {
        "log_name": "midway_tracing",
        'root_path': '/data/adn_logs/midway_tracking/',
        "log_path": '/data/adn_logs/midway_tracking/{log_type}/{log_type}.log.{cur_hour}',
        "log_params_path": "data/midway_params.config"
    },
    "4": {
        "log_name": "etl",
        'root_path': '/data/adn_logs/sync_data/receive_data',
        "log_path": '/data/adn_logs/sync_data/receive_data/receive_data_{log_type}/{cur_month}/{cur_date}/{cur_hour}.log',
        "log_params_path": "data/midway_params.config"
    }
    
}