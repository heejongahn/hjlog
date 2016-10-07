const latexExtension = (showdown) => {
  const latexInlineRegex = /(\s)~D([^~D\n].*[^~D\n])~D/g
  const latexDisplayRegex =/~D~D(.*)~D~D/g

    showdown.extension('latex' , () => {
      return [
        {
          type: "lang",
          filter: (text, converter, options) => {
            return text.replace(latexInlineRegex, (match, space, exp) => {
              return `${space}<span class="latex">${exp}</span>`;
            });
          }
        },
        {
          type: "lang",
          filter: (text, converter, options) => {
            return text.replace(latexDisplayRegex, (match, exp) => {
              return `<span class="latex-display">${exp}</span>`;
            });
          }
        }
      ];
  });
}

export default latexExtension




