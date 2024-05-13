import abc
import asyncio
import httpx


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient() as client:
        max_retries = 5
        delay_between_retries = 1

        async with httpx.AsyncClient() as client:
            for attempt in range(1, max_retries + 1):
                try:
                    response = await client.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.content
                    observer.observe(data)
                    return
                except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                    if attempt == max_retries:
                        raise
                    await asyncio.sleep(delay_between_retries)
