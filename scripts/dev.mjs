import {spawn} from 'node:child_process';
const backend=spawn('python3',['apps/api/main.py','serve'],{stdio:'inherit'});
const frontend=spawn(process.execPath,['node_modules/vite/bin/vite.js','--config','apps/web/vite.config.ts'],{stdio:'inherit'});
let stopping=false;
function stop(code=0){if(stopping)return;stopping=true;backend.kill('SIGTERM');frontend.kill('SIGTERM');setTimeout(()=>process.exit(code),100);}
backend.on('exit',code=>stop(code??1));frontend.on('exit',code=>stop(code??1));process.on('SIGINT',()=>stop());process.on('SIGTERM',()=>stop());
