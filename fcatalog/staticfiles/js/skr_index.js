
let fuse;
const input = document.getElementById("input_search");
const resultsContainer = document.getElementById("disciplines_container");

if (input) {
    fuse = new Fuse(disciplines, {
        keys: ["teacher", "title", "description"],
        includeScore: true,
        threshold: 0.4
    });
    document.getElementById("search").addEventListener("click", searchDisciplines);
}

function searchDisciplines() {
    const query = input.value.trim();
    let results;

    if (query === "") {
        results = disciplines;
    } else {
        results = fuse.search(query, { limit: disciplines.length })
            .sort((a, b) => a.score - b.score)
            .map(r => r.item);
    }

    renderResults(results);
}

function renderResults(list) {
    resultsContainer.innerHTML = "";
    list.forEach(item => {
        const block = document.createElement("div");
        block.innerHTML = `
            <p>${item.teacher}</p>
            <p>${item.title}</p>
            <p>${item.description}</p>
            <hr>
        `;
        resultsContainer.appendChild(block);
    });
}
