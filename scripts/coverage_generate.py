import subprocess
import sys


def run_pytest():
    """执行 pytest 并返回结果"""
    # 构建 pytest 命令
    pytest_args = ["pytest"]

    # 添加自定义参数（例如：指定测试目录、覆盖率选项等）
    pytest_args.extend([
        "--cov=src",  # 测量 your_package 的覆盖率
        "--cov-report=html",  # 生成 HTML 覆盖率报告
        "--cov-report=xml",
        "--cov-fail-under=80",  # 覆盖率低于 80% 时失败
        "tests/"  # 测试目录
    ])

    # 执行 pytest 命令
    result = subprocess.run(pytest_args, capture_output=True, text=True)

    # 输出结果
    print("Pytest 标准输出:")
    print(result.stdout)

    if result.stderr:
        print("Pytest 错误输出:")
        print(result.stderr)

    # 返回退出码
    return result.returncode


if __name__ == "__main__":
    exit_code = run_pytest()
    sys.exit(exit_code)
