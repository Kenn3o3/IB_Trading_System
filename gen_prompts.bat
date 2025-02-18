@echo off
echo Starting prompt generation process...
python tools\files_log_gen.py code
python tools\prompts_gen.py
echo Success: All prompt files generated!
pause