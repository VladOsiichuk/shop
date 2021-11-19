import asyncio
import os

import pytest


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker("asyncio")
        if not hasattr(item, "module"):
            continue

        module_path = os.path.relpath(
            item.module.__file__,
            os.path.commonprefix([__file__, item.module.__file__]),
        )
        module_root_dir = module_path.split(os.pathsep)[0]

        if module_root_dir.startswith("integration"):
            item.add_marker(pytest.mark.integration)
        elif module_root_dir.startswith("unit"):
            item.add_marker(pytest.mark.unit)
        else:
            raise RuntimeError(
                f"Unknown test type (filename = {module_path})",
            )
