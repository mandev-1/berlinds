name = piscineds
ENV_FILE = .env

BLUE=\033[1;34m
GRAY=\033[1;90m
NC=\033[0m

.PHONY: setup ex00 ex01 ex02 pgadmin

setup:
	@curl -Ls https://astral.sh/uv/install.sh | sh
	@export PATH="$$HOME/.local/bin:$$PATH"

ex00:
	@echo "$(BLUE)Generating pie chart...$(NC)"
	@uv run ex00/pie.py
	@echo "$(BLUE)Starting HTTP server at http://localhost:8000/pie_chart.png$(NC)"
	@cd generated && python3 -m http.server 8000

ex01:
	@echo "$(BLUE)Generating 3 charts...$(NC)"
	@uv run ex01/chart.py

	@echo "\n\n$(BLUE)Charts available at:$(NC)"
	@echo "💁 - Cstmr flow     $(BLUE)http://localhost:8000/customer_flow.png$(NC)"
	@echo "📈 - Sales          $(BLUE)http://localhost:8000/sales_monthly.png$(NC)"
	@echo "💸 - Average sp     $(BLUE)http://localhost:8000/avg_spend_monthly.png$(NC)\n\n"
	@cd generated && python3 -m http.server 8000


ex02:
	@echo "$(BLUE)Generating price statistics and boxplots...$(NC)"
	@uv run ex02/mustache.py

	@echo "\n\n$(BLUE)Charts available at:$(NC)"
	@echo "📦🟩 - Item prices boxplot 1         $(BLUE)http://localhost:8000/boxplot_item_prices.png$(NC)"
	@echo "📦📈 - Item prices boxplot 2         $(BLUE)http://localhost:8000/boxplot_item_prices-2.png$(NC)"
	@echo "🧺👤 - Avg basket per user boxplot   $(BLUE)http://localhost:8000/boxplot_avg_basket_per_user.png$(NC)\n\n"
	@cd generated && python3 -m http.server 8000

pgadmin:
	@echo "Visit http://localhost:10000 to access pgAdmin"
