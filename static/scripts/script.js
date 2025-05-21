(() => {
  'use strict';
  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => localStorage.setItem('theme', theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const setTheme = (theme) => {
    if (theme === 'auto') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-bs-theme', systemTheme);
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme);
    }
  };

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitcher = document.querySelector('#bd-theme');
    if (!themeSwitcher) return;

    themeSwitcher.setAttribute('aria-label', theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme');

    if (theme === 'dark') {
      themeSwitcherText.textContent = 'Dark Theme';
      document.getElementById("bd-theme").classList.remove("btn-light")
      
    } else {
      themeSwitcherText.textContent = 'Light Theme';
      document.getElementById("bd-theme").classList.replace("btn-secondary","btn-light")
    }

    if (focus) themeSwitcher.focus();
  };

  const toggleDarkMode = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
    setStoredTheme(newTheme);
    setTheme(newTheme);
    showActiveTheme(newTheme);
  };

  window.toggleDarkMode = toggleDarkMode;

  setTheme(getPreferredTheme());

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme();
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme());
    }
  });

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme());

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener('click', () => {
          const theme = toggle.getAttribute('data-bs-theme-value');
          setStoredTheme(theme);
          setTheme(theme);
          showActiveTheme(theme, true);
        });
      });
  });
})();


function sendMessage() {
    fetch('/recv_msg', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: document.getElementById('send_msg').value, country: document.getElementById('send_ctry').value })
    })
    .then(response => {
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            return response.json();
        } else {
            return {};
        }
    })
    .then(data => {
        alert("Thank you!");
        window.location.reload();

    })
    .catch(error => {
        alert("Error sending message.");
        console.error('Error sending message:', error);
    });
}

function printMessages() {
    fetch('/get_msgs')
        .then(response => {
            const contentType = response.headers.get("Content-Type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return response.json();
            } else {
                return [];
            }
        })
        .then(data => {
            const container = document.getElementById('messages');
            container.innerHTML = '';

            const row = document.createElement('div');
            row.className = 'row';

            data.forEach(msg => {
                const col = document.createElement('div');
                // fix to my liking
                col.className = 'col-md-6 mb-3 g-2';

                col.innerHTML = `
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">${msg.country}</h5>
      <p class="card-text">${msg.message}</p>
    </div>
  </div>`;

                row.appendChild(col);
            });
            container.appendChild(row);
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
}