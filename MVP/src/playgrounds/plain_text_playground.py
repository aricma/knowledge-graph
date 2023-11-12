from misc.constants import TEMP_STORAGE_DIRECTORY_PATH, TEMP_FILE_LOADER_DIRECTORY_PATH
from playgrounds.file_adder import FileAdder
from playgrounds.utils import format_query_results

if __name__ == '__main__':
    fa = FileAdder(
        storage_directory=str(TEMP_STORAGE_DIRECTORY_PATH),
        file_loader_temp_directory=str(TEMP_FILE_LOADER_DIRECTORY_PATH),
    )

    file_names = [
        "honey-never-spoils.txt",
        "octopuses-have-three-hearts.txt",
        "bananas-are-berries.txt",
        "the-eiffel-tower-can-grow.txt",
        "venus-rotation.txt",
    ]

    file_content = [
        "Honey Never Spoils: Archaeologists have discovered pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible. Honey's longevity can be attributed to its unique composition, which is naturally low in moisture and high in sugar, making it an inhospitable environment for bacteria and microorganisms. Additionally, honey is acidic and contains small amounts of hydrogen peroxide, which also inhibit growth of microbes.",
        "Octopuses Have Three Hearts: An octopus has a complex circulatory system with three hearts. Two of these hearts are responsible for pumping blood to the gills, while the third heart circulates it to the rest of the body. Interestingly, when an octopus swims, the heart that delivers blood to the body stops beating, which is why these creatures prefer crawling than swimming as it's less tiring.",
        "Bananas Are Berries, But Strawberries Aren't: In botanical terms, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh. Under this definition, bananas qualify as berries, but strawberries do not. Strawberries are actually considered 'aggregate fruits' because they form from a flower with multiple ovaries.",
        "The Eiffel Tower Can Grow: The Eiffel Tower in Paris, made of iron, can grow by up to six inches during the summer. When a substance is heated, its particles move more and it takes up a larger volume – this is known as thermal expansion. Conversely, the tower shrinks in the cold. Despite this expansion and contraction, the Eiffel Tower's height is officially listed as 324 meters (1,063 feet).",
        "Venus' Rotation: Venus is the only planet in the solar system that rotates clockwise on its axis. This is known as retrograde rotation and is quite unusual when compared to the rotation of most other planets. Additionally, a day on Venus (one complete rotation on its axis) is longer than a year on Venus (one complete orbit around the Sun).",
    ]

    added_files = [
        fa.add_file(
            name=name,
            file=bytes(content.encode("utf8"))
        ) for name, content in zip(file_names, file_content)
    ]

    queries = [
        "does honey spoil",
        "is venus made of honey?",
        "does venus rotate around honey?",
        "I want to go to paris!",
    ]

    for query in queries:
        results = fa.query(query)
        print(format_query_results(results))

    # teardown
    for response in added_files:
        fa.remove_file(response.storage_id)
