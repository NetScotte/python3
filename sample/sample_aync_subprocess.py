import asyncio


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f"{cmd!r} exit code: {proc.returncode}")

    if stdout:
        print(f"[stdout]: \n{stdout.decode()}")
    if stderr:
        print(f"[stderr]: \n{stderr.decode()}")



asyncio.run(run("ls /haha"))