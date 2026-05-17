import chromadb
from src.config import CHROMA_COLLECTION

CITY_DOCUMENTS = {
    "paris": [
        "Paris is the capital of France, known as the City of Light. It sits on the Seine River and has been a major European city since the 3rd century. The city's 20 arrondissements spiral outward from the Île de la Cité like a snail shell.",
        "Landmarks include the Eiffel Tower built in 1889, the Louvre Museum housing the Mona Lisa, Notre-Dame Cathedral, Arc de Triomphe, and Sacré-Cœur Basilica in Montmartre. The Champs-Élysées stretches from Place de la Concorde to the Arc.",
        "Parisian cuisine is world-renowned: croissants and café au lait for breakfast, crêpes from street vendors, coq au vin, duck confit, escargot, ratatouille, and macarons from Ladurée. The city has over 40 Michelin-starred restaurants.",
        "Best areas to stay: Le Marais for trendy boutiques and nightlife, Saint-Germain-des-Prés for literary cafés, Montmartre for artistic charm, the Latin Quarter for budget travelers, and the 7th arrondissement for Eiffel Tower proximity.",
        "Travel tips: Buy a carnet of 10 metro tickets for savings. Most museums are free the first Sunday of each month. Tipping is included in the bill (service compris). Learn basic French phrases. Avoid eating near major tourist sites for better quality and prices.",
        "Paris is ideal for couples, art enthusiasts, foodies, and history lovers. Spring (April–June) and fall (September–October) are the best seasons. The city hosts events like Paris Fashion Week, Fête de la Musique, and Nuit Blanche.",
    ],
    "tokyo": [
        "Tokyo is Japan's capital and the world's most populous metropolitan area with over 37 million people. Originally a fishing village called Edo, it became the political center in 1603 under Tokugawa Ieyasu and was renamed Tokyo in 1868 during the Meiji Restoration.",
        "Must-see landmarks: Senso-ji Temple in Asakusa (Tokyo's oldest temple), Meiji Shrine surrounded by forest, Tokyo Skytree (634m), Shibuya Crossing (world's busiest intersection), the Imperial Palace, Tsukiji Outer Market, and Akihabara's electric town.",
        "Tokyo's food scene is the best in the world with over 200 Michelin stars. Try fresh sushi at Tsukiji, ramen in tiny counter shops, tempura, wagyu beef, takoyaki, matcha desserts, and izakaya pub food. Convenience store onigiri and bento are surprisingly excellent.",
        "Best neighborhoods: Shinjuku for nightlife and entertainment, Shibuya for youth culture, Harajuku for fashion, Asakusa for traditional culture, Roppongi for international dining, Ginza for luxury shopping, and Shimokitazawa for indie vibes.",
        "Travel tips: Get a Suica/Pasmo card for seamless transit. Bow when greeting. Remove shoes before entering homes and some restaurants. Carry cash — many places don't accept cards. Trains stop around midnight. The JR Pass saves money on bullet trains.",
        "Tokyo is perfect for tech enthusiasts, anime fans, food lovers, and anyone who appreciates the blend of ultra-modern and deeply traditional. Cherry blossom season (late March–April) and autumn foliage (November) are peak times to visit.",
    ],
    "new york": [
        "New York City is the most populous city in the United States with over 8.3 million residents across five boroughs: Manhattan, Brooklyn, Queens, the Bronx, and Staten Island. Founded as New Amsterdam by Dutch colonists in 1626, it became New York in 1664.",
        "Iconic landmarks: Statue of Liberty, Empire State Building, Central Park (843 acres of green space), Times Square, Brooklyn Bridge, One World Trade Center, the Metropolitan Museum of Art, and Grand Central Terminal. Broadway hosts over 40 theaters.",
        "NYC's food is incredibly diverse: dollar pizza slices, bagels with lox, pastrami sandwiches from Katz's Deli, dim sum in Chinatown, halal cart food, craft cocktails in speakeasies, and Michelin-starred tasting menus. Every cuisine on Earth is represented.",
        "Best areas: SoHo for shopping and galleries, Greenwich Village for charm and jazz clubs, Williamsburg for hipster culture, Upper West Side for museums and families, Lower East Side for nightlife, DUMBO for waterfront views and art, Harlem for jazz and soul food.",
        "Travel tips: Buy an unlimited MetroCard for subway savings. Walk whenever possible — NYC is very walkable. Avoid Times Square restaurants. Book Broadway shows via TKTS booth for discounts. Tipping is expected (18-20%). Museums often have pay-what-you-wish hours.",
        "New York is ideal for ambitious creatives, culture seekers, foodies, and urban explorers. Fall (September–November) offers perfect weather and fewer crowds. Summer brings free concerts in Central Park, outdoor movies, and rooftop bar season.",
    ],
}


def build_vector_store() -> chromadb.Collection:
    client = chromadb.Client()
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(name=CHROMA_COLLECTION)
    ids, documents, metadatas = [], [], []
    for city, docs in CITY_DOCUMENTS.items():
        for i, doc in enumerate(docs):
            ids.append(f"{city}_{i}")
            documents.append(doc)
            metadatas.append({"city": city, "chunk_index": i})
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return collection


def query_vector_store(collection: chromadb.Collection, city: str, n_results: int = 6) -> list[str]:
    results = collection.query(
        query_texts=[f"Travel information about {city}"],
        n_results=n_results,
        where={"city": city},
    )
    return results["documents"][0] if results["documents"] else []
