const markdownInput = document.getElementById("markdown-input");
const htmlOutput = document.getElementById("html-output");
const preview = document.getElementById("preview");

function convertMarkdown() {
  let text = markdownInput.value;

  const lines = text.split("\n");
  let result = "";

  for (let line of lines) {

    // h3
    line = line.replace(/^\s*###\s+(.*)/, "<h3>$1</h3>");

    // h2
    line = line.replace(/^\s*##\s+(.*)/, "<h2>$1</h2>");

    // h1
    line = line.replace(/^\s*#\s+(.*)/, "<h1>$1</h1>");

    // blockquote
    line = line.replace(/^\s*>\s+(.*)/, "<blockquote>$1</blockquote>");

    result += line;
  }

  // images
  result = result.replace(
    /!\[([^\]]+)\]\(([^)]+)\)/g,
    '<img alt="$1" src="$2">'
  );

  // links
  result = result.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2">$1</a>'
  );

  // bold **text**
  result = result.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // bold __text__
  result = result.replace(/__(.*?)__/g, "<strong>$1</strong>");

  // italic *text*
  result = result.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // italic _text_
  result = result.replace(/_(.*?)_/g, "<em>$1</em>");

  return result;
}

markdownInput.addEventListener("input", () => {
  const html = convertMarkdown();

  htmlOutput.textContent = html; // raw HTML
  preview.innerHTML = html;      // rendered HTML
});