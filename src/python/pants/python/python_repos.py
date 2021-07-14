# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import logging

from pex.fetcher import Fetcher, PyPIFetcher
from pex.http import RequestsContext, StreamFilelike, requests

from pants.subsystem.subsystem import Subsystem
from pants.util.memo import memoized_method

logger = logging.getLogger(__name__)


# TODO: These methods of RequestsContext are monkey-patched out to work around
# https://github.com/pantsbuild/pex/issues/26: we should upstream a fix for this.
_REQUESTS_TIMEOUTS = (15, 30)


def _open_monkey(self, link):
    # requests does not support file:// -- so we must short-circuit manually
    if link.local:
        return open(link.local_path, "rb")  # noqa: T802
    for attempt in range(self._max_retries + 1):
        try:
            return StreamFilelike(
                self._session.get(
                    link.url,
                    verify=self._verify,
                    stream=True,
                    headers={"User-Agent": self.USER_AGENT},
                    timeout=_REQUESTS_TIMEOUTS,
                ),
                link,
            )
        except requests.exceptions.ReadTimeout:
            # Connect timeouts are handled by the HTTPAdapter, unfortunately read timeouts are not
            # so we'll retry them ourselves.
            logger.warning(
                f"Read timeout trying to fetch {link.url}, retrying. "
                f"{self._max_retries - attempt} retries remain."
            )
        except requests.exceptions.RequestException as e:
            raise self.Error(e)

    raise self.Error(
        requests.packages.urllib3.exceptions.MaxRetryError(
            None, link, "Exceeded max retries of %d" % self._max_retries
        )
    )


def _resolve_monkey(self, link):
    return link.wrap(
        self._session.head(
            link.url,
            verify=self._verify,
            allow_redirects=True,
            headers={"User-Agent": self.USER_AGENT},
            timeout=_REQUESTS_TIMEOUTS,
        ).url
    )


def _make_create_session_patcher(trust_env):
    @staticmethod
    def _create_session_monkey(max_retries):
        session = requests.session()
        session.trust_env = trust_env
        retrying_adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        session.mount('http://', retrying_adapter)
        session.mount('https://', retrying_adapter)
        return session

    return _create_session_monkey


RequestsContext.open = _open_monkey
RequestsContext.resolve = _resolve_monkey


class PythonRepos(Subsystem):
    """A python code repository.

    Note that this is part of the Pants core, and not the python backend, because it's used to
    bootstrap Pants plugins.
    """

    options_scope = "python-repos"

    @classmethod
    def register_options(cls, register):
        super().register_options(register)
        register(
            "--repos",
            advanced=True,
            type=list,
            default=[],
            fingerprint=True,
            help="URLs of code repositories.",
        )
        register(
            "--indexes",
            advanced=True,
            type=list,
            fingerprint=True,
            default=["https://pypi.org/simple/"],
            help="URLs of code repository indexes.",
        )
        register(
            "--trust-env",
            advanced=True,
            type=bool,
            default=False,
            help="requests.Session trust_env attribute."
        )


    @property
    def repos(self):
        return self.get_options().repos

    @property
    def indexes(self):
        return self.get_options().indexes

    @memoized_method
    def get_fetchers(self):
        fetchers = []
        fetchers.extend(Fetcher([url]) for url in self.repos)
        fetchers.extend(PyPIFetcher(url) for url in self.indexes)
        return fetchers

    @memoized_method
    def get_network_context(self):
        # TODO(wickman): Add retry, conn_timeout, threads, etc configuration here.
        RequestsContext._create_session = _make_create_session_patcher(self.get_options().trust_env)
        return RequestsContext()
