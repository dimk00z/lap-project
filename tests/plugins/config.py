DATABASE_PATH = "/tmp/test.sqlite"


# def cleanup_db():
#     if os.path.exists(DATABASE_PATH):
#         os.remove(DATABASE_PATH)


# @pytest.fixture(autouse=True)
# def _use_sqlite(mocker) -> Generator[None, None, None]:
#     """Use sqlite in memory for testing."""
#     mocker.patch(
#         "server.config.PostgresConfig.connection_string",
#         new_callable=mocker.PropertyMock,
#         return_value=f"sqlite+aiosqlite:///{DATABASE_PATH}",
#     )
#     yield
#     cleanup_db()
