export function detect_browser() {
  let isES6 = true;

  try {
    new Function("(a = 0) => a");
  } catch (e) {
    isES6 = false;
  }

  if (typeof Symbol === "undefined" || !("from" in Array) || !("assign" in Object)) {
    isES6 = false;
  }

  // Cegah redirect berulang pakai localStorage
  if (localStorage.getItem("alreadyRedirected")) {
    console.log("Redirect sudah pernah dilakukan, tidak diulang.");
    return;
  }

  const resultDiv = document.getElementById("result");
  if (resultDiv) {
    if (isES6) {
      // 
      console.log("Browser mendukung ES6.");

      // Tandai supaya tidak redirect lagi
      localStorage.setItem("alreadyRedirected", "true");
      window.location.href = "/";
    } 
    
    else {
      // 
      console.log("Browser ini hanya mendukung ES5 atau lebih lama.");

      // Muat polyfill dulu
      const polyfillScript = document.createElement("script");

      polyfillScript.src = "/static/polyfill/minified.js";
      polyfillScript.onload = function () {
        // 
        console.log("Custom polyfill dimuat.");
        
        // Setelah polyfill siap, redirect
        localStorage.setItem("alreadyRedirected", "true");
        window.location.href = "/unsupported";
      };

      document.head.appendChild(polyfillScript);
    }
  }
}