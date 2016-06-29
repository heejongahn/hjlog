const figureExtension = (showdown) => {
  const figure = `<figure><img src="`
  const imgRegex = /(?:<p>)?<img.*?src="(.+?)".*?alt="(.*?)"(.*?)\/?>(?:<\/p>)?/gi;
  showdown.extension('figure', () => {
    return [
      {
        type: "output",
        filter: (text, converter, options) => {
          return text.replace(imgRegex, (match, url, alt, rest) => {
            return `<figure><img src="${url}" alt="${alt}" title="${alt}"><figcaption>${alt}</figcaption></figure>`;
          });
        }
      }
    ];
  });
}

export default figureExtension;
