document.addEventListener("DOMContentLoaded", function() {
    const subjectBoxes = document.querySelectorAll(".subject-box");

    subjectBoxes.forEach(box => {
        box.addEventListener("click", function() {
            const nombre = this.getAttribute("data-nombre") || "No disponible";
            const semestre = this.getAttribute("data-semestre") || "No disponible";
            const codigo = this.getAttribute("data-codigo") || "No disponible";
            const creditos = this.getAttribute("data-creditos") || "No disponible";
            const requisitos = this.getAttribute("data-requisitos") || "No disponible";
            const bibliografia = this.getAttribute("data-bibliografia");
            const material = this.getAttribute("data-material");

            document.getElementById("modalNombre").textContent = nombre;
            document.getElementById("modalSemestre").textContent = semestre;
            document.getElementById("modalCodigo").textContent = codigo;
            document.getElementById("modalCreditos").textContent = creditos;
            document.getElementById("modalRequisitos").textContent = requisitos;
            document.getElementById("modalBibliografia").innerHTML = bibliografia;

            if (material) {
                document.getElementById("modalMaterial").href = material;
                document.getElementById("modalMaterial").textContent = "Ver Material";
                document.getElementById("modalMaterialContainer").style.display = "block";
            } else {
                document.getElementById("modalMaterialContainer").style.display = "none";
            }

            var myModal = new bootstrap.Modal(document.getElementById('subjectModal'));
            myModal.show();
        });
    });
});