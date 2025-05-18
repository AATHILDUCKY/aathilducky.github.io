document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("keyword-input");
  const tagContainer = document.getElementById("selected-tags");
  const notes = [...document.querySelectorAll(".note")];

  // Create floating suggestion box
  const suggestionBox = document.createElement("div");
  suggestionBox.style.position = "fixed";
  suggestionBox.style.top = "15px";
  suggestionBox.style.right = "15px";
  suggestionBox.style.maxWidth = "200px";
  suggestionBox.style.maxHeight = "300px";
  suggestionBox.style.overflowY = "auto";
  suggestionBox.style.opacity = "0.5";
  suggestionBox.style.zIndex = "9999";
  suggestionBox.className = "bg-[#161b22] text-sm border border-gray-700 rounded p-2 shadow-md";
  document.body.appendChild(suggestionBox);

  let tags = [];
  let allKeywords = new Set();

  // Extract keywords from notes: titles, tags, and content
  notes.forEach(note => {
    const noteTags = note.dataset.tags.split(',').map(t => t.trim().toLowerCase());
    const noteTitle = note.dataset.title.toLowerCase();
    const noteContent = note.querySelector(".obsidian-style")?.innerText.toLowerCase() || "";

    noteTags.forEach(tag => allKeywords.add(tag));
    noteTitle.split(/\s+/).forEach(word => allKeywords.add(word));
    noteContent.split(/\s+/).forEach(word => {
      if (word.length > 2) allKeywords.add(word);
    });
  });

  allKeywords = Array.from(allKeywords).filter(word => word.length > 1);

  function renderTags() {
    tagContainer.innerHTML = "";
    tags.forEach((tag, index) => {
      const span = document.createElement("span");
      span.className = "tag bg-[#21262d] text-white px-2 py-1 rounded flex items-center";
      span.innerHTML = `${tag} <span class="remove ml-2 cursor-pointer text-red-400" data-index="${index}">x</span>`;
      tagContainer.appendChild(span);
    });
    filterNotes();
  }

  function filterNotes() {
    notes.forEach(note => {
      const noteTags = note.dataset.tags.split(",").map(t => t.trim());
      const noteTitle = note.dataset.title.toLowerCase();
      const noteContent = note.querySelector(".obsidian-style")?.innerText.toLowerCase() || "";

      let matchCount = 0;
      tags.forEach(tag => {
        if (
          noteTags.includes(tag) ||
          noteTitle.includes(tag) ||
          noteContent.includes(tag)
        ) {
          matchCount++;
        }
      });

      note.dataset.match = matchCount;
      note.style.display = matchCount > 0 || tags.length === 0 ? "block" : "none";
    });

    notes
      .sort((a, b) => b.dataset.match - a.dataset.match)
      .forEach(note => note.parentNode.appendChild(note));
  }

  input.addEventListener("input", function () {
    const value = input.value.trim().toLowerCase();
    suggestionBox.innerHTML = "";

    if (value) {
      const suggestions = allKeywords
        .filter(k => k.startsWith(value) && !tags.includes(k))
        .slice(0, 10);

      suggestions.forEach(suggestion => {
        const div = document.createElement("div");
        div.className = "cursor-pointer hover:bg-[#30363d] p-1 rounded text-white";
        div.textContent = suggestion;
        div.addEventListener("click", () => {
          tags.push(suggestion);
          input.value = "";
          renderTags();
          suggestionBox.innerHTML = "";
        });
        suggestionBox.appendChild(div);
      });
    }
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      const value = input.value.trim().toLowerCase().replace(/,$/, "");
      if (value && !tags.includes(value)) {
        tags.push(value);
        renderTags();
      }
      input.value = "";
      suggestionBox.innerHTML = "";
    }
  });

  tagContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove")) {
      const index = e.target.dataset.index;
      tags.splice(index, 1);
      renderTags();
    }
  });
});
