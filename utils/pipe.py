from typing import Any, Awaitable, Callable, Iterable, Literal, Tuple

def pipe(
    fns: Iterable[Callable[
        ...,  
        Tuple[Literal[False], dict] |
        Tuple[Literal[True], Tuple]
    ]],
    final_fn: Callable[
        ...,
        Tuple[Literal[False], dict] |
        Tuple[Literal[True], dict | None]
    ],
    *init_args: Any
):
    ret_args = init_args
    for fn in fns:
        pack = fn(*ret_args)

        if pack[0] == False:
            return pack[1]

        ret_args = pack[1]

    pack = final_fn(*ret_args)

    if pack[0] == False:
        return pack[1]

    [_, more_entries] = pack
    body = { 'status': 'ok' }

    if more_entries is None:
        return body
    return body | more_entries

async def pipe_async(
    fns: Iterable[Callable[
        ...,
        Awaitable[
            Tuple[Literal[False], dict] |
            Tuple[Literal[True], Tuple]
        ]
    ]],
    final_fn: Callable[
        ...,
        Awaitable[
            Tuple[Literal[False], dict] |
            Tuple[Literal[True], dict | None]
        ]
    ],
    *init_args: Any
):
    ret_args = init_args
    for fn in fns:
        pack = await fn(*ret_args)

        if pack[0] == False:
            return pack[1]

        ret_args = pack[1]

    pack = await final_fn(*ret_args)

    if pack[0] == False:
        return pack[1]

    [_, more_entries] = pack
    body = { 'status': 'ok' }

    if more_entries is None:
        return body
    return body | more_entries
