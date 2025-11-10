// Authentication functionality
let isLoggedIn = false
let currentUser = null

// Debug logging
console.log("Auth.js loaded successfully!")

// Check login status on page load
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM Content Loaded - Setting up event listeners")
  checkLoginStatus()
  setupEventListeners()
})

function checkLoginStatus() {
  const user = localStorage.getItem("user")
  if (user) {
    isLoggedIn = true
    currentUser = JSON.parse(user)
    updateNavigation()
  }
}

function updateNavigation() {
  const navButtons = document.getElementById("nav-buttons")
  const heroButtons = document.getElementById("hero-buttons")
  const ctaButtons = document.getElementById("cta-buttons")

  if (isLoggedIn) {
    navButtons.innerHTML = `
            <a href="dashboard.html" class="px-4 py-2 gradient-bg text-white rounded-lg hover:shadow-lg transition-all">Dashboard</a>
        `
    heroButtons.innerHTML = `
            <a href="dashboard.html" class="px-6 py-3 gradient-bg text-white rounded-lg hover:shadow-lg transition-all text-lg">Go to Dashboard</a>
            <a href="dashboard.html" class="px-6 py-3 border-2 border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition-all text-lg">Nutrition Filter</a>
        `
    ctaButtons.innerHTML = `
            <a href="dashboard.html" class="px-6 py-3 bg-white text-green-600 rounded-lg hover:bg-gray-100 transition-all text-lg">Start Budget Optimizer</a>
            <a href="dashboard.html" class="px-6 py-3 border-2 border-white text-white rounded-lg hover:bg-white hover:text-green-600 transition-all text-lg">Try Nutrition Filter</a>
        `
  }
}

function setupEventListeners() {
  console.log("Setting up event listeners...")
  
  // Modal controls
  const loginModal = document.getElementById("login-modal")
  const signupModal = document.getElementById("signup-modal")
  
  console.log("Login modal found:", !!loginModal)
  console.log("Signup modal found:", !!signupModal)

  // Login buttons
  const loginBtn = document.getElementById("login-btn")
  const heroLoginBtn = document.getElementById("hero-login")
  const ctaLoginBtn = document.getElementById("cta-login")
  
  console.log("Login buttons found:", {
    loginBtn: !!loginBtn,
    heroLogin: !!heroLoginBtn,
    ctaLogin: !!ctaLoginBtn
  })
  
  loginBtn?.addEventListener("click", () => {
    console.log("Login button clicked!")
    showModal("login")
  })
  heroLoginBtn?.addEventListener("click", () => {
    console.log("Hero login button clicked!")
    showModal("login")
  })
  ctaLoginBtn?.addEventListener("click", () => {
    console.log("CTA login button clicked!")
    showModal("login")
  })

  // Signup buttons
  const signupBtn = document.getElementById("signup-btn")
  const heroSignupBtn = document.getElementById("hero-signup")
  const ctaSignupBtn = document.getElementById("cta-signup")
  
  console.log("Signup buttons found:", {
    signupBtn: !!signupBtn,
    heroSignup: !!heroSignupBtn,
    ctaSignup: !!ctaSignupBtn
  })
  
  signupBtn?.addEventListener("click", () => {
    console.log("Signup button clicked!")
    showModal("signup")
  })
  heroSignupBtn?.addEventListener("click", () => {
    console.log("Hero signup button clicked!")
    showModal("signup")
  })
  ctaSignupBtn?.addEventListener("click", () => {
    console.log("CTA signup button clicked!")
    showModal("signup")
  })

  // Close buttons
  const closeLoginBtn = document.getElementById("close-login")
  const closeSignupBtn = document.getElementById("close-signup")
  
  closeLoginBtn?.addEventListener("click", () => {
    console.log("Close login button clicked!")
    hideModal("login")
  })
  closeSignupBtn?.addEventListener("click", () => {
    console.log("Close signup button clicked!")
    hideModal("signup")
  })

  // Switch between modals
  const switchToSignupBtn = document.getElementById("switch-to-signup")
  const switchToLoginBtn = document.getElementById("switch-to-login")
  
  switchToSignupBtn?.addEventListener("click", () => {
    console.log("Switch to signup clicked!")
    hideModal("login")
    showModal("signup")
  })
  switchToLoginBtn?.addEventListener("click", () => {
    console.log("Switch to login clicked!")
    hideModal("signup")
    showModal("login")
  })

  // Demo login button
  const demoLoginBtn = document.getElementById("demo-login-btn")
  console.log("Demo login button found:", !!demoLoginBtn)
  
  demoLoginBtn?.addEventListener("click", () => {
    console.log("Demo login button clicked!")
    demoLogin()
  })

  // Form submissions
  const loginForm = document.getElementById("login-form")
  const signupForm = document.getElementById("signup-form")
  
  console.log("Forms found:", {
    loginForm: !!loginForm,
    signupForm: !!signupForm
  })
  
  loginForm?.addEventListener("submit", (e) => {
    console.log("Login form submitted!")
    handleLogin(e)
  })
  signupForm?.addEventListener("submit", (e) => {
    console.log("Signup form submitted!")
    handleSignup(e)
  })

  // Close modal when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal")) {
      console.log("Modal background clicked, closing modal")
      event.target.classList.remove("show")
    }
  })

  // Add smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href'))
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    })
  })
  
  console.log("Event listeners setup complete!")
}

function showModal(type) {
  console.log(`Showing modal: ${type}`)
  const modal = document.getElementById(`${type}-modal`)
  if (modal) {
    modal.classList.add("show")
    console.log(`Modal ${type} shown successfully`)
    // Focus on first input
    const firstInput = modal.querySelector('input')
    if (firstInput) {
      firstInput.focus()
    }
  } else {
    console.error(`Modal ${type} not found!`)
  }
}

function hideModal(type) {
  const modal = document.getElementById(`${type}-modal`)
  if (modal) {
    modal.classList.remove("show")
    // Clear form
    const form = modal.querySelector('form')
    if (form) {
      form.reset()
    }
  }
}

async function handleLogin(e) {
  e.preventDefault()
  const formData = new FormData(e.target)
  const email = formData.get("email")
  const password = formData.get("password")

  if (!email || !password) {
    alert("Please fill in all fields")
    return
  }

  try {
    console.log("Attempting login with:", { email, password })
    
    const response = await fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    })

        console.log("Response status:", response.status)
    const result = await response.json()
    console.log("Login result:", result)
    if (result.success) {
      localStorage.setItem("user", JSON.stringify(result.user))
      isLoggedIn = true
      currentUser = result.user
      hideModal("login")
      showSuccessMessage("Login successful! Redirecting to dashboard...")
      setTimeout(() => {
        window.location.href = "dashboard.html"
      }, 1500)
    } else {
      showErrorMessage(result.message || "Login failed. Please try again.")
    }
  } catch (error) {
    console.error("Login error:", error)
    showErrorMessage("Login failed. Please check your connection and try again.")
  }
}

async function handleSignup(e) {
  e.preventDefault()
  const formData = new FormData(e.target)
  const name = formData.get("name")
  const email = formData.get("email")
  const password = formData.get("password")

  if (!name || !email || !password) {
    alert("Please fill in all fields")
    return
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters long")
    return
  }

  try {
    console.log("Attempting signup with:", { name, email, password })
    
    const response = await fetch("http://localhost:5000/api/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    })

        console.log("Signup response status:", response.status)
    const result = await response.json()
    console.log("Signup result:", result)
    if (result.success) {
      localStorage.setItem("user", JSON.stringify(result.user))
      isLoggedIn = true
      currentUser = result.user
      hideModal("signup")
      showSuccessMessage("Account created successfully! Redirecting to dashboard...")
      setTimeout(() => {
        window.location.href = "dashboard.html"
      }, 1500)
    } else {
      showErrorMessage(result.message || "Signup failed. Please try again.")
    }
  } catch (error) {
    console.error("Signup error:", error)
    showErrorMessage("Signup failed. Please check your connection and try again.")
  }
}

function showSuccessMessage(message) {
  showMessage(message, "success")
}

function showErrorMessage(message) {
  showMessage(message, "error")
}

function showMessage(message, type) {
  // Remove existing messages
  const existingMessage = document.querySelector('.message-popup')
  if (existingMessage) {
    existingMessage.remove()
  }

  // Create message element
  const messageDiv = document.createElement('div')
  messageDiv.className = `message-popup fixed top-20 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300 ${
    type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
  }`
  messageDiv.textContent = message

  document.body.appendChild(messageDiv)

  // Remove message after 3 seconds
  setTimeout(() => {
    messageDiv.style.opacity = "0"
    setTimeout(() => {
      if (messageDiv.parentNode) {
        messageDiv.parentNode.removeChild(messageDiv)
      }
    }, 300)
  }, 3000)
}

// Add demo login functionality for testing
function demoLogin() {
  console.log("Demo login function called!")
  
  // Use the test account from database
  const demoUser = {
    id: 1,
    name: "Test User",
    email: "test@example.com"
  }
  
  console.log("Setting demo user:", demoUser)
  
  localStorage.setItem("user", JSON.stringify(demoUser))
  isLoggedIn = true
  currentUser = demoUser
  
  console.log("User logged in, updating navigation...")
  updateNavigation()
  
  console.log("Showing success message...")
  showSuccessMessage("Demo login successful!")
  
  console.log("Demo login complete, redirecting...")
  setTimeout(() => {
    window.location.href = "dashboard.html"
  }, 1500)
}

// Add logout function that clears token
function logout() {
  localStorage.removeItem("user")
  localStorage.removeItem("token")
  isLoggedIn = false
  currentUser = null
  updateNavigation()
  showSuccessMessage("Logged out successfully!")
  setTimeout(() => {
    window.location.href = "index.html"
  }, 1000)
}

// Make demo login available globally for testing
window.demoLogin = demoLogin
