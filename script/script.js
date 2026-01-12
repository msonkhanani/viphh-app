const searchInput = document.getElementById("search");
const resultsList = document.getElementById("results");

searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length < 2) {
        resultsList.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        resultsList.innerHTML = "";
        data.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.household_head} | ${item.household_id} | ${item.village}`;
            resultsList.appendChild(li);
        });

    } catch (error) {
        console.error("Error fetching search results:", error);
        resultsList.innerHTML = "<li>Error loading results</li>";
    }
});
