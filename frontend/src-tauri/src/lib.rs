use std::sync::Mutex;
use tauri::{Emitter, Manager};
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

#[tauri::command]
fn get_backend_port(state: tauri::State<Mutex<Option<u16>>>) -> Option<u16> {
    *state.lock().unwrap()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(Mutex::new(None::<u16>))
        .manage(Mutex::new(None::<CommandChild>))
        .invoke_handler(tauri::generate_handler![get_backend_port])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }

            let handle = app.handle().clone();
            let sidecar = app.shell().sidecar("uniclare-backend")?;
            let (mut rx, child) = sidecar.spawn()?;

            // store child so we can kill it later on window close
            let child_state = app.state::<Mutex<Option<CommandChild>>>();
            *child_state.lock().unwrap() = Some(child);

            tauri::async_runtime::spawn(async move {
                while let Some(event) = rx.recv().await {
                    match event {
                        CommandEvent::Stdout(line) => {
                            let line = String::from_utf8_lossy(&line);
                            log::info!("[backend] {}", line.trim());
                            if let Some(port_str) = line.trim().strip_prefix("PORT=") {
                                if let Ok(port) = port_str.parse::<u16>() {
                                    let state = handle.state::<Mutex<Option<u16>>>();
                                    *state.lock().unwrap() = Some(port);
                                    handle.emit("backend-ready", port).ok();
                                }
                            }
                        }
                        CommandEvent::Stderr(line) => {
                            let line = String::from_utf8_lossy(&line);
                            log::error!("[backend] {}", line.trim());
                        }
                        _ => {}
                    }
                }
            });

            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                let state = window.state::<Mutex<Option<CommandChild>>>();
                let child = state.lock().unwrap().take();
                if let Some(child) = child {
                    let _ = child.kill();
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}