// document.getElementById("openLink").addEventListener("click", () => {
//   const input = document.getElementById("userInput").value.trim();
//   if (input) {
//     const baseUrl = "https://example.com/search?q="; // Change to your desired base URL
//     const fullUrl = baseUrl + encodeURIComponent(input);
//     chrome.tabs.create({ url: fullUrl });
//   }
// });

document.getElementById("openLink").addEventListener("click", async () => {
  const input = document.getElementById("userInput").value.trim();
  if (input) {
    const baseUrl = "file:///C:/Users/prosys301/app/app2/m1/index.html";
    const fullUrl = baseUrl + "?text=" + encodeURIComponent(input);
    let parts = input.split(/[-B]/);
    if (parts.length > 1) {
      parts[0] = '*' + parts[0];
      input = parts.join('-');
    }
    chrome.tabs.create({ url: fullUrl }, (tab) => {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (text) => {
          const container = document.createElement("div");
          container.textContent = text;
          container.style.position = "absolute";
          container.style.top = "20px";
          container.style.left = "20px";
          container.style.background = "yellow";
          container.style.padding = "10px";
          container.style.zIndex = "9999";
          document.body.appendChild(container);
        },
        args: [input]
      });
    });
  }
});

