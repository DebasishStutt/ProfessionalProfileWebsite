const widget = document.querySelector("[data-twin-widget]");

if (widget) {
  const toggle = widget.querySelector("[data-twin-toggle]");
  const closeButton = widget.querySelector("[data-twin-close]");
  const panel = widget.querySelector("[data-twin-panel]");
  const messagesEl = widget.querySelector("[data-twin-messages]");
  const form = widget.querySelector("[data-twin-form]");
  const input = widget.querySelector("[data-twin-input]");
  const status = widget.querySelector("[data-twin-status]");

  const conversation = [];
  let autoScrollEnabled = true;
  let hasWelcomed = false;

  const setStatus = (text) => {
    if (status) {
      status.textContent = text;
    }
  };

  const scrollToBottom = (force = false) => {
    if (!messagesEl) {
      return;
    }
    if (!autoScrollEnabled && !force) {
      return;
    }
    messagesEl.scrollTop = messagesEl.scrollHeight;
  };

  const isNearBottom = () => {
    if (!messagesEl) {
      return true;
    }
    const threshold = 80;
    return (
      messagesEl.scrollHeight - messagesEl.scrollTop - messagesEl.clientHeight < threshold
    );
  };

  const addMessage = (role, content, className = "") => {
    if (!messagesEl) {
      return null;
    }
    const wrapper = document.createElement("div");
    wrapper.className = `twin-message twin-${role} ${className}`.trim();
    wrapper.textContent = content;
    messagesEl.appendChild(wrapper);
    scrollToBottom(true);
    return wrapper;
  };

  const openWidget = () => {
    widget.dataset.state = "open";
    if (toggle) {
      toggle.setAttribute("aria-expanded", "true");
    }
    if (!hasWelcomed) {
      addMessage(
        "assistant",
        "Hi, I am Debasish's digital twin. Ask me about his experience, skills, or leadership."
      );
      hasWelcomed = true;
    }
    if (input) {
      input.focus();
    }
    scrollToBottom(true);
  };

  const closeWidget = () => {
    widget.dataset.state = "closed";
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
    }
    setStatus("");
  };

  if (toggle) {
    toggle.addEventListener("click", () => {
      if (widget.dataset.state === "open") {
        closeWidget();
      } else {
        openWidget();
      }
    });
  }

  if (closeButton) {
    closeButton.addEventListener("click", closeWidget);
  }

  if (messagesEl) {
    messagesEl.addEventListener("scroll", () => {
      autoScrollEnabled = isNearBottom();
    });
  }

  window.addEventListener("scroll", () => {
    if (widget.dataset.state === "open" && autoScrollEnabled) {
      scrollToBottom(true);
    }
  });

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!input) {
        return;
      }
      const message = input.value.trim();
      if (!message) {
        return;
      }
      input.value = "";
      addMessage("user", message);
      conversation.push({ role: "user", content: message });
      setStatus("Thinking...");

      const typing = addMessage("assistant", "Typing...");

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages: conversation.slice(-8),
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        if (typing && typing.parentNode) {
          typing.parentNode.removeChild(typing);
        }

        const reply = (data && data.reply ? data.reply : "").trim();
        if (!reply) {
          throw new Error("Empty reply");
        }
        addMessage("assistant", reply);
        conversation.push({ role: "assistant", content: reply });
        setStatus("");
      } catch (error) {
        if (typing && typing.parentNode) {
          typing.parentNode.removeChild(typing);
        }
        addMessage(
          "assistant",
          "I could not reach the digital twin right now. Please try again or contact via email or LinkedIn."
        );
        setStatus("Offline");
      }
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && widget.dataset.state === "open") {
      closeWidget();
    }
  });
}
