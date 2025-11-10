// Dashboard functionality
let currentTab = "overview"
let cart = []

document.addEventListener("DOMContentLoaded", () => {
  checkAuth()
  setupEventListeners()
  loadCart()
  updateCartDisplay()
})

function checkAuth() {
  const user = localStorage.getItem("user")
  if (!user) {
    window.location.href = "index.html"
    return
  }

  const userData = JSON.parse(user)
  document.getElementById("welcome-user").textContent = `Welcome, ${userData.name}`
}

function setupEventListeners() {
  // Tab navigation
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.getAttribute("data-tab")
      switchTab(tab)
    })
  })

  // Logout
  document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("user")
    localStorage.removeItem("cart")
    window.location.href = "index.html"
  })

  // Budget optimizer
  document.getElementById("optimize-btn")?.addEventListener("click", optimizeBudget)

  // Items search
  document.getElementById("search-items")?.addEventListener("input", searchItems)

  // Nutrition filter
  document.getElementById("filter-btn")?.addEventListener("click", filterNutrition)
  document.getElementById("preset-low-calorie")?.addEventListener("click", () => applyPreset("low-calorie"))
  document.getElementById("preset-high-protein")?.addEventListener("click", () => applyPreset("high-protein"))
  document.getElementById("preset-low-sugar")?.addEventListener("click", () => applyPreset("low-sugar"))
  document.getElementById("preset-low-fat")?.addEventListener("click", () => applyPreset("low-fat"))

  // Healthier swaps
  document.getElementById("find-swaps-btn")?.addEventListener("click", findSwaps)

  // Cart actions
  document.getElementById("save-basket-btn")?.addEventListener("click", saveBasket)
  document.getElementById("clear-cart-btn")?.addEventListener("click", clearCart)

  // Load initial data
  loadItems()
}

function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("tab-active")
    btn.classList.add("tab-inactive")
  })
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("tab-active")
  document.querySelector(`[data-tab="${tabName}"]`).classList.remove("tab-inactive")

  // Show/hide tab content
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.add("hidden")
  })
  document.getElementById(`${tabName}-tab`).classList.remove("hidden")

  currentTab = tabName

  if (tabName === "cart") {
    updateCartDisplay()
  }
}

// Budget Optimizer Functions
async function optimizeBudget() {
  const budget = document.getElementById("budget-input").value
  const familySize = document.getElementById("family-size").value

  if (!budget) {
    alert("Please enter a budget")
    return
  }

  const btn = document.getElementById("optimize-btn")
  btn.textContent = "Optimizing..."
  btn.disabled = true

  try {
    const response = await fetch("http://localhost:5000/api/optimize-budget", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        budget: Number.parseFloat(budget),
        familySize: Number.parseInt(familySize),
      }),
    })

    const result = await response.json()
    displayBudgetResults(result)
  } catch (error) {
    console.error("Budget optimization error:", error)
    alert("Optimization failed. Please try again.")
  } finally {
    btn.textContent = "Optimize My Budget"
    btn.disabled = false
  }
}

function displayBudgetResults(result) {
  const resultsDiv = document.getElementById("budget-results")
  const itemsDiv = document.getElementById("budget-items")
  const summaryDiv = document.getElementById("budget-summary")

  if (result.items && result.items.length > 0) {
    itemsDiv.innerHTML = result.items
      .map(
        (item) => `
            <div class="flex justify-between items-center p-3 bg-white rounded border">
                <div>
                    <div class="font-medium">${item.food}</div>
                    <div class="text-sm text-gray-600">Nutrition Score: ${item.nutrition_density?.toFixed(2) || "N/A"}</div>
                </div>
                <div class="text-right">
                    <div class="font-semibold">₹${item.price}</div>
                    <button class="mt-1 px-3 py-1 gradient-bg text-white text-sm rounded hover:shadow-lg transition-all" onclick="addToCart(${JSON.stringify(item).replace(/"/g, "&quot;")})">Add to Cart</button>
                </div>
            </div>
        `,
      )
      .join("")

    if (result.summary) {
      summaryDiv.innerHTML = `
                <div class="text-sm space-y-1">
                    <div>Total Budget: ₹${result.summary.budget}</div>
                    <div>Total Cost: ₹${result.summary.totalCost}</div>
                    <div>Savings: ₹${result.summary.savings}</div>
                </div>
            `
    }

    resultsDiv.classList.remove("hidden")
  }
}

// Items List Functions
async function loadItems() {
  try {
    const response = await fetch("http://localhost:5000/api/items")
    const data = await response.json()
    displayItems(data.items || [])
  } catch (error) {
    console.error("Failed to load items:", error)
    document.getElementById("items-list").innerHTML =
      '<div class="text-center py-8 text-red-500">Failed to load items</div>'
  }
}

function displayItems(items) {
  const itemsList = document.getElementById("items-list")
  if (items.length === 0) {
    itemsList.innerHTML = '<div class="text-center py-8 text-gray-500">No items found</div>'
    return
  }

  itemsList.innerHTML = items
    .slice(0, 50)
    .map(
      (item) => `
        <div class="flex justify-between items-center p-3 bg-gray-50 rounded border">
            <div class="flex-1">
                <div class="font-medium">${item.food}</div>
                <div class="text-sm text-gray-600">
                    Calories: ${item.caloric_value} | Protein: ${item.protein}g | Price: ₹${item.price}
                </div>
            </div>
            <button class="px-3 py-1 gradient-bg text-white text-sm rounded hover:shadow-lg transition-all" onclick="addToCart(${JSON.stringify(item).replace(/"/g, "&quot;")})">Add to Cart</button>
        </div>
    `,
    )
    .join("")
}

function searchItems() {
  const searchTerm = document.getElementById("search-items").value.toLowerCase()
  // This would filter the loaded items - simplified for demo
  loadItems() // In real implementation, filter the existing items array
}

// Nutrition Filter Functions
async function filterNutrition() {
  const filters = {
    calories: document.getElementById("calories-filter").value,
    protein: document.getElementById("protein-filter").value,
    fat: document.getElementById("fat-filter").value,
    sugars: document.getElementById("sugars-filter").value,
  }

  const btn = document.getElementById("filter-btn")
  btn.textContent = "Filtering..."
  btn.disabled = true

  try {
    const response = await fetch("http://localhost:5000/api/filter-nutrition", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(filters),
    })

    const data = await response.json()
    displayFilterResults(data.items || [])
  } catch (error) {
    console.error("Filtering error:", error)
    alert("Filtering failed. Please try again.")
  } finally {
    btn.textContent = "Apply Nutrition Filters"
    btn.disabled = false
  }
}

function displayFilterResults(items) {
  const resultsDiv = document.getElementById("filter-results")
  const itemsDiv = document.getElementById("filtered-items")
  const countDiv = document.getElementById("filter-count")

  if (items.length > 0) {
    itemsDiv.innerHTML = items
      .map(
        (item) => `
            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-lg border hover:shadow-md transition-shadow">
                <div class="flex-1">
                    <div class="font-medium text-gray-900">${item.food}</div>
                    <div class="text-sm text-gray-600 mt-1">
                        <span class="inline-flex items-center gap-1">
                            <span class="text-orange-500">🔥</span> ${item.caloric_value} cal
                        </span>
                        <span class="inline-flex items-center gap-1 ml-3">
                            <span class="text-red-500">💪</span> ${item.protein}g protein
                        </span>
                        <span class="inline-flex items-center gap-1 ml-3">
                            <span class="text-yellow-500">🧈</span> ${item.fat}g fat
                        </span>
                        <span class="inline-flex items-center gap-1 ml-3">
                            <span class="text-pink-500">🍯</span> ${item.sugars}g sugar
                        </span>
                    </div>
                    <div class="text-xs text-green-600 mt-1">Nutrition Score: ${(item.nutrition_density || 0).toFixed(2)}</div>
                </div>
                <div class="text-right ml-4">
                    <div class="font-semibold text-lg text-gray-900">₹${item.price}</div>
                    <button class="mt-2 px-4 py-2 gradient-bg text-white text-sm rounded-lg hover:shadow-lg transition-all" onclick="addToCart(${JSON.stringify(item).replace(/"/g, "&quot;")})">Add to Cart</button>
                </div>
            </div>
        `,
      )
      .join("")

    resultsDiv.classList.remove("hidden")
    countDiv.textContent = `${items.length} items found`
  } else {
    itemsDiv.innerHTML = `
        <div class="text-center py-12">
            <div class="text-4xl mb-4">🔍</div>
            <h3 class="text-lg font-semibold mb-2">No items match your filters</h3>
            <p class="text-gray-600 mb-4">Try adjusting your filter criteria or use our quick presets</p>
            <button onclick="clearFilters()" class="px-4 py-2 gradient-bg text-white rounded-lg hover:shadow-lg transition-all">Clear Filters</button>
        </div>
    `
    resultsDiv.classList.remove("hidden")
    countDiv.textContent = "0 items found"
  }
}

function applyPreset(presetType) {
  const caloriesFilter = document.getElementById("calories-filter")
  const proteinFilter = document.getElementById("protein-filter")
  const fatFilter = document.getElementById("fat-filter")
  const sugarsFilter = document.getElementById("sugars-filter")

  // Clear all filters first
  caloriesFilter.value = ""
  proteinFilter.value = ""
  fatFilter.value = ""
  sugarsFilter.value = ""

  switch (presetType) {
    case "low-calorie":
      caloriesFilter.value = "low"
      fatFilter.value = "low"
      break
    case "high-protein":
      proteinFilter.value = "high"
      break
    case "low-sugar":
      sugarsFilter.value = "low"
      break
    case "low-fat":
      fatFilter.value = "low"
      break
  }

  // Show visual feedback
  showCartNotification(`Applied ${presetType.replace("-", " ")} preset`)

  // Auto-apply the filter
  setTimeout(() => {
    filterNutrition()
  }, 500)
}

function clearFilters() {
  document.getElementById("calories-filter").value = ""
  document.getElementById("protein-filter").value = ""
  document.getElementById("fat-filter").value = ""
  document.getElementById("sugars-filter").value = ""

  // Hide results
  document.getElementById("filter-results").classList.add("hidden")

  showCartNotification("Filters cleared")
}

// Healthier Swaps Functions
async function findSwaps() {
  const food = document.getElementById("swap-food").value
  if (!food) {
    alert("Please enter a food item")
    return
  }

  const btn = document.getElementById("find-swaps-btn")
  btn.textContent = "Finding..."
  btn.disabled = true

  try {
    const response = await fetch("http://localhost:5000/api/healthier-swaps", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ food }),
    })

    const data = await response.json()
    displaySwaps(data.swaps || [])
  } catch (error) {
    console.error("Swaps error:", error)
    alert("Failed to find swaps. Please try again.")
  } finally {
    btn.textContent = "Find Swaps"
    btn.disabled = false
  }
}

function displaySwaps(swaps) {
  const resultsDiv = document.getElementById("swaps-results")
  const swapsDiv = document.getElementById("swaps-list")

  if (swaps.length > 0) {
    swapsDiv.innerHTML = swaps
      .map(
        (swap) => `
            <div class="flex justify-between items-center p-4 bg-green-50 rounded border border-green-200">
                <div class="flex-1">
                    <div class="font-medium text-green-800">${swap.food}</div>
                    <div class="text-sm text-green-600">
                        Similarity Score: ${swap.similarity?.toFixed(2) || "N/A"} | Nutrition Density: ${swap.nutrition_density?.toFixed(2) || "N/A"}
                    </div>
                    <div class="text-xs text-gray-600 mt-1">
                        Cal: ${swap.caloric_value} | Protein: ${swap.protein}g | Fat: ${swap.fat}g
                    </div>
                </div>
                <div class="text-right">
                    <div class="font-semibold">₹${swap.price}</div>
                    <button class="mt-1 px-3 py-1 gradient-bg text-white text-sm rounded hover:shadow-lg transition-all" onclick="addToCart(${JSON.stringify(swap).replace(/"/g, "&quot;")})">Add to Cart</button>
                </div>
            </div>
        `,
      )
      .join("")

    resultsDiv.classList.remove("hidden")
  } else {
    swapsDiv.innerHTML = '<div class="text-center py-8 text-gray-500">No healthier alternatives found</div>'
    resultsDiv.classList.remove("hidden")
  }
}

// Cart Functions
function loadCart() {
  const cartData = localStorage.getItem("cart")
  cart = cartData ? JSON.parse(cartData) : []
}

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart))
  updateCartDisplay()
  updateCartBadge()
}

function addToCart(item) {
  if (!item.food_id && item.food) {
    item.food_id = item.food.toLowerCase().replace(/\s+/g, "_") + "_" + Date.now()
  }

  const existingItem = cart.find((cartItem) => cartItem.food_id === item.food_id || cartItem.food === item.food)

  if (existingItem) {
    existingItem.quantity += 1
  } else {
    cart.push({ ...item, quantity: 1 })
  }

  saveCart()

  showCartNotification(`${item.food} added to cart!`)

  // Uncomment the line below if you want to auto-switch to cart
  // switchTab('cart')
}

function showCartNotification(message) {
  // Create notification element
  const notification = document.createElement("div")
  notification.className =
    "fixed top-20 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300"
  notification.textContent = message

  document.body.appendChild(notification)

  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.style.opacity = "0"
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}

function updateCartBadge() {
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)

  // Update cart tab text to show item count
  const cartTab = document.querySelector('[data-tab="cart"]')
  if (cartTab) {
    const cartText = cartTab.querySelector("span:last-child")
    if (cartText) {
      cartText.textContent = totalItems > 0 ? `Cart (${totalItems})` : "Cart"
    }
  }
}

function updateCartDisplay() {
  const emptyCart = document.getElementById("empty-cart")
  const cartItems = document.getElementById("cart-items")
  const cartSummary = document.getElementById("cart-summary")

  if (cart.length === 0) {
    emptyCart?.classList.remove("hidden")
    cartItems?.classList.add("hidden")
    cartSummary?.classList.add("hidden")
    updateCartBadge()
    return
  }

  emptyCart?.classList.add("hidden")
  cartItems?.classList.remove("hidden")
  cartSummary?.classList.remove("hidden")

  // Display cart items
  if (cartItems) {
    cartItems.innerHTML = cart
      .map(
        (item, index) => `
        <div class="flex justify-between items-center p-4 bg-gray-50 rounded border">
            <div class="flex-1">
                <div class="font-medium">${item.food}</div>
                <div class="text-sm text-gray-600">
                    ₹${item.price} each | Cal: ${item.caloric_value} | Protein: ${item.protein}g
                </div>
            </div>
            <div class="flex items-center gap-3">
                <div class="flex items-center gap-2">
                    <button onclick="updateQuantity(${index}, ${item.quantity - 1})" class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300">-</button>
                    <span class="w-8 text-center">${item.quantity}</span>
                    <button onclick="updateQuantity(${index}, ${item.quantity + 1})" class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300">+</button>
                </div>
                <div class="text-right min-w-16">
                    <div class="font-semibold">₹${(Number.parseFloat(item.price) * item.quantity).toFixed(2)}</div>
                </div>
                <button onclick="removeItem(${index})" class="text-red-500 hover:text-red-700 ml-2">&times;</button>
            </div>
        </div>
    `,
      )
      .join("")
  }

  // Update summary
  const total = cart.reduce((sum, item) => sum + Number.parseFloat(item.price) * item.quantity, 0)
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)
  const avgPrice = totalItems > 0 ? total / totalItems : 0

  const cartTotalEl = document.getElementById("cart-total")
  const totalItemsEl = document.getElementById("total-items")
  const avgPriceEl = document.getElementById("avg-price")

  if (cartTotalEl) cartTotalEl.textContent = total.toFixed(2)
  if (totalItemsEl) totalItemsEl.textContent = totalItems
  if (avgPriceEl) avgPriceEl.textContent = avgPrice.toFixed(2)

  // Update stats in overview
  const itemsCountEl = document.getElementById("items-count")
  const budgetUsedEl = document.getElementById("budget-used")

  if (itemsCountEl) itemsCountEl.textContent = totalItems
  if (budgetUsedEl) budgetUsedEl.textContent = `₹${total.toFixed(2)}`

  updateCartBadge()
}

function updateQuantity(index, newQuantity) {
  if (newQuantity <= 0) {
    removeItem(index)
    return
  }

  cart[index].quantity = newQuantity
  saveCart()
}

function removeItem(index) {
  const removedItem = cart[index]
  showCartNotification(`${removedItem.food} removed from cart`)

  cart.splice(index, 1)
  saveCart()
}

async function saveBasket() {
  try {
    const user = JSON.parse(localStorage.getItem("user"))
    const total = cart.reduce((sum, item) => sum + Number.parseFloat(item.price) * item.quantity, 0)

    const response = await fetch("http://localhost:5000/api/save-basket", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: user.id,
        items: cart,
        total: total,
      }),
    })

    const result = await response.json()
    if (result.success) {
      alert("Basket saved successfully!")
    } else {
      alert("Failed to save basket")
    }
  } catch (error) {
    console.error("Save basket error:", error)
    alert("Failed to save basket")
  }
}

function clearCart() {
  if (cart.length > 0 && !confirm("Are you sure you want to clear your cart?")) {
    return
  }

  cart = []
  saveCart()
  showCartNotification("Cart cleared")
}

// Make functions globally available
window.switchTab = switchTab
window.addToCart = addToCart
window.updateQuantity = updateQuantity
window.removeItem = removeItem
window.applyPreset = applyPreset
window.clearFilters = clearFilters
