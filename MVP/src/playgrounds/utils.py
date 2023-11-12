from typing import List

from playgrounds.models import QueryResult


def format_query_result(query_result: QueryResult) -> List[str]:
    query = f"Query: \"{query_result.query}\""
    dub_line = '=' * 120
    line = "-" * 120
    output_block = [
        dub_line,
        query,
        line,
    ]
    for match_index, match in enumerate(query_result.matching_chunks):
        rank = match_index + 1
        match = f"{rank}: \"{match.content}\""
        output_block.append(match)
    source = f"Source: \"{query_result.original_file}\""
    output_block = [
        *output_block,
        source,
        "",
    ]
    return output_block


def format_query_results(query_results: List[QueryResult]) -> str:
    output_blocks = list()
    for result_index, query_result in enumerate(query_results):
        output_blocks = [
            *output_blocks,
            *format_query_result(query_result),
        ]
    return f"\n\n".join(output_blocks)
