// electron-app/main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const spawn = require('cross-spawn');
const waitOn = require('wait-on');

let backendProcess = null;
let mainWindow = null;

function startBackend() {
  let exeName = process.platform === "win32" ? "run_uvicorn.exe" : "run_uvicorn";

  // When packaged, executable lives in process.resourcesPath/resources/
  const exePath = path.join(process.resourcesPath, "resources", exeName);

  console.log("Starting backend from:", exePath);

  backendProcess = spawn(exePath, [], {
    stdio: "inherit"
  });

  backendProcess.on("error", (err) => {
    console.error("Failed to start backend:", err);
  });

  backendProcess.on("exit", (code) => {
    console.log("Backend exited with code", code);
  });
}


function stopBackend() {
  if (backendProcess && !backendProcess.killed) {
    try {
      backendProcess.kill();
    } catch (e) {
      console.warn('Error killing backend:', e);
    }
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 400,
    height: 200,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Wait for backend to be ready, then load renderer that calls it
  waitOn({ resources: ['http://127.0.0.1:8000/hello'], timeout: 15000 }, (err) => {
    if (err) {
      console.error('Backend not available:', err);
      // still load renderer so user sees error
      mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
      return;
    }
    mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  });

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startBackend();
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  // On macOS, apps usually stay open until quit; here we quit.
  stopBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  } else {
    app.quit();
  }
});

app.on('quit', () => {
  stopBackend();
});
