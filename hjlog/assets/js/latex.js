const latexExtension = (showdown) => {
  const latexInlineRegex = /\s~D([^~D\n].*[^~D\n])~D/g
  const latexDisplayRegex =/~D~D(.*)~D~D/g
    showdown.extension('latex' , () => {
      return [
        {
          type: "lang",
          filter: (text, converter, options) => {
            return text.replace(latexInlineRegex, (match, exp) => {
              return `<span class="latex"> ${exp}</span>`;
            });
          }
        },
        {
          type: "lang",
          filter: (text, converter, options) => {
            return text.replace(latexDisplayRegex, (match, exp) => {
              return `<div class="latex">${exp}</div>`;
            });
          }
        }
      ];
  });
}

export default latexExtension




