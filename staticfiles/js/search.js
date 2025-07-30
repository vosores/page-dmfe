document.getElementById("search-btn").addEventListener("click", function () {
    const searchTerm = document.getElementById("search-input").value.toLowerCase();
    if (!searchTerm) return;

    // Limpia resultados anteriores
    const elements = document.querySelectorAll(".highlight");
    elements.forEach((el) => {
        el.classList.remove("highlight");
    });

    // Busca coincidencias en todo el contenido de la página
    const bodyText = document.body.innerHTML;
    const regex = new RegExp(`(${searchTerm})`, "gi");

    document.body.innerHTML = bodyText.replace(
        regex,
        '<span class="highlight">$1</span>'
    );
});

// Estilo para resaltar coincidencias
const style = document.createElement("style");
style.innerHTML = `
    .highlight {
        background-color: yellow;
        color: black;
    }
`;
document.head.appendChild(style);