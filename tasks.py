"""
Automate deployment to PyPi
"""

import invoke


@invoke.task
def clean(ctx):
    """
    Clean up build and dist before building submittion to pypi
    """
    ctx.run("rm -rf build/* dist/*")


@invoke.task
def check_for_unstaged_changes(ctx):
    """
    If unstaged changes raise an error
    """
    try:
        ctx.run("git diff-index --quiet HEAD")
    except invoke.exceptions.UnexpectedExit as error:
        print(("ERROR: There are unstaged changes."))
        raise error
    except Exception as error:
        raise error


@invoke.task(pre=[check_for_unstaged_changes, clean])
def deploy_patch(ctx):
    """
    Automate deployment to pypi
    """
    ctx.run("bumpversion patch --verbose")
    ctx.run("python3 setup.py sdist bdist_wheel")
    ctx.run("twine check dist/*")
    ctx.run("twine upload dist/*")
    ctx.run("git push --tags")


@invoke.task(pre=[check_for_unstaged_changes, clean])
def first_deploy(ctx):
    """
    First deployment to pypi
    """
    ctx.run("python3 setup.py sdist bdist_wheel")
    ctx.run("twine check dist/*")
    ctx.run("twine upload dist/*")
    ctx.run("git tag 'v0.1.0'")
    ctx.run("git push --tags")
