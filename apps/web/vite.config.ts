import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
export default defineConfig({root:fileURLToPath(new URL('.',import.meta.url)),plugins:[react()],server:{host:'127.0.0.1',port:5173,strictPort:true,proxy:{'/api':'http://127.0.0.1:8000'}},build:{outDir:'dist',emptyOutDir:true,rolldownOptions:{output:{codeSplitting:{groups:[{name:'translations',test:/packages[\/]i18n[\/]locales[\/]/,priority:20}]}}}}});
