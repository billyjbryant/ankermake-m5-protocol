from jsonrpc import dispatcher
from flask import current_app as app

import web.util


@dispatcher.add_method(name="server.connection.identify")
def server_connection_identify(client_name, version, type, url, access_token=None, api_key=None):
    return {
        "connection_id": id(id),
    }


@dispatcher.add_method(name="server.announcements.list")
def server_announcements_list(include_dismissed=True):
    return {
        "entries": [],
        "feeds": [
            "moonraker",
            "klipper",
            "moonlight"
        ]
    }


@dispatcher.add_method(name="server.info")
def server_info():
    return {
        "klippy_connected": True,
        "klippy_state": "ready",
        "components": [
            "file_manager",
            "update_manager",
            "announcements",
            "authorization",
            "button",
            "data_store",
            "database",
            "dbus_manager",
            "extensions",
            "gpio",
            "history",
            "http_client",
            "job_queue",
            "job_state",
            "klippy_apis",
            "ldap",
            "machine",
            "mqtt",
            "notifier",
            "octoprint_compat",
            "paneldue",
            "power",
            "proc_stats",
            "secrets",
            "sensor",
            "shell_command",
            "simplyprint",
            "template",
            "webcam",
            "wled",
            "zeroconf",
        ],
        "failed_components": [],
        "registered_directories": ["config", "gcodes", "config_examples", "docs"],
        "warnings": [],
        "websocket_count": 2,
        "moonraker_version": "v0.7.1-797",
        "api_version": [1, 2, 1],
        "api_version_string": "1.2.1"
    }


@dispatcher.add_method(name="server.history.list")
def server_history_list(start=0, limit=50, before=None, since=None, order="desc"):
    return {
        "count": 1,
        "jobs": [
            {
                "job_id": "000001",
                "exists": True,
                "end_time": 1615764265.6493807,
                "filament_used": 7.83,
                "filename": "test/history_test.gcode",
                "metadata": {
                    # Object containing metadata at time of job
                },
                "print_duration": 18.37201827496756,
                "status": "completed",
                "start_time": 1615764496.622146,
                "total_duration": 18.37201827496756
            },
        ]
    }


@dispatcher.add_method(name="server.history.totals")
def server_history_totals():
    return {
        "job_totals": {
            "total_jobs": 3,
            "total_time": 11748.077333278954,
            "total_print_time": 11348.794790096988,
            "total_filament_used": 11615.718840001999,
            "longest_job": 11665.191012736992,
            "longest_print": 11348.794790096988
        }
    }


@dispatcher.add_method(name="server.gcode_store")
def server_gcode_store(count=1000):
    return {
        "gcode_store": [
            {
                "message": "FIRMWARE_RESTART",
                "time": 1615832299.1167388,
                "type": "command"
            },
            {
                "message": "// Klipper state: Ready",
                "time": 1615832309.9977088,
                "type": "response"
            },
            {
                "message": "M117 This is a test",
                "time": 1615834094.8662775,
                "type": "command"
            },
            {
                "message": "G4 P1000",
                "time": 1615834098.761729,
                "type": "command"
            },
            {
                "message": "STATUS",
                "time": 1615834104.2860553,
                "type": "command"
            },
            {
                "message": "// Klipper state: Ready",
                "time": 1615834104.3299904,
                "type": "response"
            }
        ]
    }


@dispatcher.add_method(name="server.temperature_store")
def server_temperature_store():
    with app.svc.borrow("updates") as upd:
        return {
            "extruder": {
                "temperatures": [h.current for h in upd.pstats.nozzle],
                "targets": [h.target for h in upd.pstats.nozzle],
            },
            "heater_bed": {
                "temperatures": [h.current for h in upd.pstats.hotbed],
                "targets": [h.target for h in upd.pstats.hotbed],
            },
        }


@dispatcher.add_method(name="server.config")
def server_config():
    host, port = web.util.get_host_port(app)

    return {
        "config": {
            "server": {
                "host": host,
                "port": port,
                "ssl_port": port,
                "enable_debug_logging": True,
                "enable_asyncio_debug": True,
                "klippy_uds_address": "/tmp/klippy_uds",
                "max_upload_size": 1024,
                "ssl_certificate_path": None,
                "ssl_key_path": None
            },
            "dbus_manager": {},
            "database": {
                # "database_path": "~/.moonraker_database",
                "database_path": None,
                "enable_database_debug": False
            },
            "file_manager": {
                "enable_object_processing": True,
                "queue_gcode_uploads": False,
                "config_path": None, #"~/printer_config",
                "log_path": None, #"~/logs"
            },
            "klippy_apis": {},
            "machine": {
                "provider": "systemd_dbus"
            },
            "shell_command": {},
            "data_store": {
                "temperature_store_size": 1200,
                "gcode_store_size": 1000
            },
            "proc_stats": {},
            "job_state": {},
            "job_queue": {
                "load_on_startup": False,
                "automatic_transition": False,
                "job_transition_delay": 2,
                "job_transition_gcode": "\nM118 Transitioning to next job..."
            },
            "http_client": {},
            "announcements": {
                "dev_mode": False,
                "subscriptions": [
                    "mainsail",
                ]
            },
            "authorization": {
                "login_timeout": 90,
                "force_logins": False,
                "default_source": "moonraker",
                "enable_api_key": True,
                "cors_domains": [
                    "*"
                ],
                "trusted_clients": [
                    "0.0.0.0/0"
                ]
            },
            "zeroconf": {},
            "octoprint_compat": {
                "enable_ufp": True,
                "flip_h": False,
                "flip_v": False,
                "rotate_90": False,
                "stream_url": f"ws://{host}:{port}/ws/video",
                "webcam_enabled": True
            },
            "history": {},
            "secrets": {
                "secrets_path": "~/moonraker_secrets.ini"
            },
            "mqtt": {
                # "address": "eric-work.home",
                # "port": 1883,
                # "username": "{secrets.mqtt_credentials.username}",
                # "password_file": None,
                # "password": "{secrets.mqtt_credentials.password}",
                # "mqtt_protocol": "v3.1.1",
                # "instance_name": "pi-debugger",
                # "default_qos": 0,
                # "status_objects": {
                #     "webhooks": None,
                #     "toolhead": "position,print_time",
                #     "idle_timeout": "state",
                #     "gcode_macro M118": None
                # },
                # "api_qos": 0,
                # "enable_moonraker_api": True
            },
            "template": {}
        },
        "orig": {
            "DEFAULT": {},
            "server": {
                "enable_debug_logging": "True",
                "max_upload_size": "210"
            },
            "file_manager": {
                # "config_path": "~/printer_config",
                # "log_path": "~/logs",
                # "queue_gcode_uploads": "True",
                "enable_object_processing": "True"
            },
            "machine": {
                "provider": "systemd_dbus"
            },
            "announcements": {},
            "job_queue": {
                "job_transition_delay": "2.",
                "job_transition_gcode": "\nM118 Transitioning to next job...",
                "load_on_startup": "True"
            },
            # "authorization": {
            #     "trusted_clients": "\n192.168.1.0/24",
            #     #                    "cors_domains": "\n*.home\nhttp://my.mainsail.xyz\nhttp://app.fluidd.xyz\n*://localhost:*"
            #     },
            "zeroconf": {},
            "octoprint_compat": {},
            "authorization": {
                "force_logins": "False",
                "default_source": "moonraker",
                "trusted_clients": "\n0.0.0.0/0",
                "cors_domains": "\n*"
            },
            "history": {},
            "secrets": {
                "secrets_path": "~/moonraker_secrets.ini"
            },
            "mqtt": {
                "address": "eric-work.home",
                "port": "1883",
                "username": "{secrets.mqtt_credentials.username}",
                "password": "{secrets.mqtt_credentials.password}",
                "enable_moonraker_api": True,
                #                    "status_objects": "\nwebhooks\ntoolhead=position,print_time\nidle_timeout=state\ngcode_macro M118"
            }
        },
        "files": [
            {
                "filename": "moonraker.conf",
                "sections": [
                    "server",
                    "file_manager",
                    "machine",
                    "announcements",
                    "job_queue",
                    "authorization",
                    "zeroconf",
                    "octoprint_compat",
                    "history",
                    "secrets"
                ]
            },
            {
                "filename": "include/extras.conf",
                "sections": [
                    "mqtt"
                ]
            }
        ]
    }


@dispatcher.add_method(name="server.webcams.list")
def server_webcams_list():
    host, port = web.util.get_host_port(app)

    return {
        "webcams": [
            {
                "name": "Printer",
                "location": "printer",
                "service": "jmuxer-stream",
                "enabled": True,
                "icon": "mdiWebcam",
                "target_fps": 15,
                "target_fps_idle": 5,
                "stream_url": f"ws://{host}:{port}/ws/video",
                "snapshot_url": "",
                "flip_horizontal": False,
                "flip_vertical": False,
                "rotation": 0,
                "aspect_ratio": "4:3",
                "source": "config"
            }
        ]
    }


@dispatcher.add_method(name="server.logs.rollover")
def server_logs_rollover(application):
    ...
