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


@invoke.task
def bump_patch(ctx):
    """
    Bump version by patch
    """
    ctx.run("bumpversion patch --verbose")


@invoke.task
def bump_minor(ctx):
    """
    Bump version by minor
    """
    ctx.run("bumpversion minor --verbose")


@invoke.task(pre=[check_for_unstaged_changes, clean])
def build_distribution(ctx):
    """
    Use twine to build a distribution
    """
    ctx.run("python3 setup.py sdist bdist_wheel")
    ctx.run("twine check dist/*")
    ctx.run("twine upload dist/*")


@invoke.task(pre=[bump_patch, build_distribution])
def deploy_patch(ctx):
    """
    Automate deployment to pypi
    """
    ctx.run("git push --tags")


@invoke.task(pre=[bump_minor, build_distribution])
def deploy_minor(ctx):
    """
    Automate deployment to pypi
    """
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
