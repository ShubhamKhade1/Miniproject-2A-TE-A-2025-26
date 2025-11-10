# 🧑‍💻 ShopSmart AI: Copilot Instructions for AI Coding Agents

## Big Picture Architecture

- **Frontend**: Pure HTML/CSS/JS (no framework), main files: `index.html`, `dashboard.html`, `dashboard.js`, `auth.js`, `globals.css`.
- **Backend**: Flask app (`simple_app.py`) with REST API endpoints for cart, basket, and KNN-powered recommendations. No persistent backend required for demo mode.
- **Database**: MySQL schema in `simple_database.sql`, updated via `update_database.py`. Multi-basket support: each basket is a transaction for Apriori analysis.
- **AI/ML**: KNN algorithm for healthier swaps (see `KNN_IMPLEMENTATION.md`). Apriori algorithm for basket analysis (see `MULTI_BASKET_README.md`).
- **Demo Mode**: No authentication or backend required; use sample data for full feature testing.

## Developer Workflows

- **Run Flask backend**: `python simple_app.py`
- **Update DB schema**: `python update_database.py`
- **Test KNN**: `python test_knn.py`
- **Test multi-basket**: `python test_multi_basket.py`
- **Frontend testing**: Open `index.html` in browser; use Demo Login for full access.

## Project-Specific Patterns & Conventions

- **Basket Saving**: Each save creates a new basket (see `MULTI_BASKET_README.md`). Naming modal, historical basket view, and load-to-cart features.
- **KNN Healthier Swaps**: Uses 11 nutrition features, cosine similarity, and nutrition density for ranking. See `KNN_IMPLEMENTATION.md` for API and scoring details.
- **API Endpoints**: `/api/cart/save`, `/api/cart/saved-baskets`, `/api/healthier-swaps` (see markdown docs for payloads).
- **Testing**: Scripts are Python files, run directly. Manual UI testing via browser; automated via test scripts.
- **Keyboard Shortcuts**: `Ctrl+7` for Saved Baskets tab, `Ctrl+1-6` for other tabs, `Escape` to close modals.
- **Notifications**: Success/error/info messages auto-dismiss after 3s.

## Integration Points & Dependencies

- **Python**: Flask, pandas, scikit-learn, mlxtend (see `requirements.txt`)
- **Database**: MySQL (local, demo, or cloud)
- **Data Files**: Nutrition datasets (`cleaned_nutrition_dataset_with_price.csv`, `nutrition_with_co2.csv`)
- **Frontend**: No build step; static files only.

## Key Files & Directories

- `simple_app.py`: Flask backend, API endpoints
- `dashboard.js`, `auth.js`: Frontend logic
- `simple_database.sql`: DB schema
- `update_database.py`: DB migration
- `KNN_IMPLEMENTATION.md`, `MULTI_BASKET_README.md`: AI/ML and basket logic
- `test_knn.py`, `test_multi_basket.py`: Automated tests

## Example: Save Basket API

```http
POST /api/cart/save
{
  "user_id": 1,
  "cart_name": "Weekly Groceries",
  "items": [ ... ]
}
```

---

For unclear workflows or missing conventions, ask the user for clarification or examples before making assumptions.
