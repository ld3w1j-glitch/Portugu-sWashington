(() => {
    const root = document.documentElement;
    const storedTheme = localStorage.getItem("gramatica-theme");
    if (storedTheme) root.dataset.theme = storedTheme;

    const themeButton = document.querySelector(".theme-toggle");
    const themeIcon = document.querySelector(".theme-icon");
    const refreshThemeIcon = () => {
        if (themeIcon) themeIcon.textContent = root.dataset.theme === "light" ? "☀" : "☾";
    };
    refreshThemeIcon();
    themeButton?.addEventListener("click", () => {
        root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
        localStorage.setItem("gramatica-theme", root.dataset.theme);
        refreshThemeIcon();
    });

    const menuButton = document.querySelector(".menu-toggle");
    const menu = document.querySelector(".main-nav");
    menuButton?.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("open");
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    const showToast = (message) => {
        const region = document.querySelector("#toast-region");
        if (!region) return;
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = message;
        region.append(toast);
        window.setTimeout(() => toast.remove(), 3200);
    };

    const textarea = document.querySelector("#sentence");
    const count = document.querySelector(".char-count span");
    if (textarea && count) {
        const updateCount = () => { count.textContent = textarea.value.length; };
        textarea.addEventListener("input", updateCount);
        document.querySelectorAll("[data-example]").forEach((button) => {
            button.addEventListener("click", () => {
                textarea.value = button.dataset.example;
                updateCount();
                textarea.focus();
            });
        });
    }

    const wordDetail = document.querySelector("#word-detail");
    document.querySelectorAll(".analysis-token").forEach((tokenButton) => {
        tokenButton.addEventListener("click", () => {
            document.querySelectorAll(".analysis-token").forEach((item) => item.classList.remove("selected"));
            tokenButton.classList.add("selected");
            const item = JSON.parse(tokenButton.dataset.details);
            const tags = (item.morfologia || []).map((value) => `<span>${escapeHtml(value)}</span>`).join("");
            const alternatives = item.alternativas?.length
                ? `<div class="detail-alternatives"><small>Outras leituras possíveis</small><p>${item.alternativas.map(escapeHtml).join(" · ")}</p></div>`
                : "";
            wordDetail.className = "word-detail";
            wordDetail.dataset.class = item.classe;
            wordDetail.innerHTML = `
                <span class="detail-class">${escapeHtml(item.classe)} · ${item.confianca}% de confiança</span>
                <h4>${escapeHtml(item.token)} <small>${escapeHtml(item.subclasse || "")}</small></h4>
                <p>${escapeHtml(item.explicacao)}</p>
                <div class="detail-tags">${tags}</div>
                <div class="detail-function">
                    <small>Função sintática nesta frase</small>
                    <strong>${escapeHtml(item.funcao)}</strong>
                    <p>Classe e função são informações diferentes: a classe descreve a palavra; a função descreve seu trabalho na oração.</p>
                </div>
                ${alternatives}
            `;
        });
    });

    document.querySelectorAll(".quiz-box").forEach((quiz) => {
        const correctIndex = Number(quiz.dataset.answer);
        const feedback = quiz.querySelector(".quiz-feedback");
        quiz.querySelectorAll(".quiz-options button").forEach((button) => {
            button.addEventListener("click", async () => {
                if (quiz.dataset.answered === "true") return;
                quiz.dataset.answered = "true";
                const index = Number(button.dataset.index);
                const correct = index === correctIndex;
                button.classList.add(correct ? "correct" : "wrong");
                quiz.querySelector(`[data-index="${correctIndex}"]`)?.classList.add("correct");
                feedback.className = `quiz-feedback show ${correct ? "correct" : "wrong"}`;
                feedback.innerHTML = `<strong>${correct ? "Resposta correta." : "Vamos rever."}</strong> ${escapeHtml(feedback.dataset.explanation)}`;
                try {
                    await fetch("/api/progresso", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            lesson_id: quiz.dataset.lessonId,
                            completed: correct,
                            score: correct ? 100 : 0,
                        }),
                    });
                } catch (_) {
                    showToast("O resultado aparecerá nesta tela, mas não pôde ser salvo agora.");
                }
            });
        });
    });

    document.querySelector(".complete-lesson")?.addEventListener("click", async (event) => {
        const button = event.currentTarget;
        try {
            const response = await fetch("/api/progresso", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lesson_id: button.dataset.lessonId, completed: true, score: 0}),
            });
            if (!response.ok) throw new Error();
            button.textContent = "Aula concluída ✓";
            showToast("Progresso salvo.");
        } catch (_) {
            showToast("Não foi possível salvar o progresso.");
        }
    });

    const exerciseCards = [...document.querySelectorAll(".exercise-card")];
    const scoreValue = document.querySelector(".exercise-score h2 strong");
    const scoreBar = document.querySelector(".score-bar span");
    const refreshScore = () => {
        const correct = exerciseCards.filter((card) => card.dataset.correct === "true").length;
        if (scoreValue) scoreValue.textContent = String(correct);
        if (scoreBar) scoreBar.style.width = `${exerciseCards.length ? correct / exerciseCards.length * 100 : 0}%`;
    };

    exerciseCards.forEach((card) => {
        card.querySelectorAll(".exercise-options button").forEach((button) => {
            button.addEventListener("click", async () => {
                if (card.dataset.answered === "true") return;
                card.dataset.answered = "true";
                const chosen = button.dataset.value;
                const feedback = card.querySelector(".exercise-feedback");
                button.classList.add("selected");
                try {
                    const response = await fetch("/api/tentativa", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            exercise_id: Number(card.dataset.exerciseId),
                            answer: chosen,
                        }),
                    });
                    const result = await response.json();
                    if (!response.ok) throw new Error(result.error);
                    card.dataset.correct = String(result.correct);
                    button.classList.add(result.correct ? "correct" : "wrong");
                    card.querySelectorAll(".exercise-options button").forEach((candidate) => {
                        if (candidate.dataset.value === result.answer) candidate.classList.add("correct");
                    });
                    feedback.className = `exercise-feedback show ${result.correct ? "correct" : "wrong"}`;
                    feedback.innerHTML = `<strong>${result.correct ? "Correto." : `Resposta: ${escapeHtml(result.answer)}.`}</strong> ${escapeHtml(result.explanation)}`;
                    refreshScore();
                } catch (_) {
                    card.dataset.answered = "false";
                    showToast("Não foi possível registrar esta resposta.");
                }
            });
        });
    });

    document.querySelector(".print-button")?.addEventListener("click", () => {
        const answerKey = document.querySelector("#print-answer-key");
        document.body.classList.toggle("include-answer-key", Boolean(answerKey?.checked));
        window.print();
    });

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }
})();
