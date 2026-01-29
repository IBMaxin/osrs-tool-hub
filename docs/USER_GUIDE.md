# OSRS Tool Hub - User Guide

Welcome to OSRS Tool Hub! This guide will help you get started with all the features available in the application.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Flipping Calculator](#flipping-calculator)
3. [Gear Calculator](#gear-calculator)
4. [Slayer Tracker](#slayer-tracker)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [FAQ](#faq)

## Getting Started

### First Visit

When you first visit OSRS Tool Hub, a unique user ID is automatically generated and stored in your browser's localStorage. This ID is used to:
- Track your trades and watchlist items
- Maintain your personal statistics
- Keep your data separate from other users

**Note**: Your user ID is stored locally in your browser. If you clear your browser data, you'll get a new user ID and lose access to your previous data.

### Navigation

The application features a hierarchical navigation menu:
- **Flipping** → Scanner, Profit Tracker, Trade History
- **Gear** → Loadout Builder, DPS Lab, Progression
- **Slayer** → Task Advisor, Monster Database

## Flipping Calculator

The Flipping Calculator helps you find profitable Grand Exchange (GE) trading opportunities.

### Finding Flip Opportunities

1. Navigate to **Flipping → Scanner**
2. Use the filter controls to set your preferences:
   - **Max Budget**: Maximum GP you're willing to invest (100K - 100M)
   - **Min ROI**: Minimum return on investment percentage (0% - 20%)
   - **Min Volume**: Minimum trade volume requirement
3. Results automatically update as you adjust filters
4. Click the **Refresh** button (or press `R`) to update prices

### Understanding Flip Results

Each flip opportunity shows:
- **Item Name**: The OSRS item
- **Buy Price**: Current GE buy price
- **Sell Price**: Current GE sell price
- **Profit**: Profit per item after tax
- **ROI**: Return on investment percentage
- **Volume**: Current trade volume
- **Limit**: GE trade limit for the item

**Tax Calculation**: The tool automatically accounts for GE tax (2% with a 5M cap).

### Logging Trades

1. Navigate to **Flipping → My Trades**
2. Click **Log Trade** button (or use the quick log button from flip results)
3. Fill in the trade details:
   - **Item**: Search and select the item
   - **Buy Price**: Price per item when bought
   - **Quantity**: Number of items
   - **Sell Price**: (Optional) Price per item when sold
   - **Status**: Choose "bought", "sold", or "cancelled"
4. Click **Log Trade** to save

### Trade History

View all your logged trades in the **My Trades** tab:
- Filter by status (bought/sold/cancelled)
- Filter by item
- Filter by date range
- Sort by any column

### Trade Statistics

Navigate to **Flipping → Stats** to see:
- **Total Profit**: Sum of all profitable trades
- **Total Trades**: Number of trades logged
- **Sold Trades**: Number of completed trades
- **Profit Per Hour**: Estimated profit rate
- **Best Items**: Top performing items by profit
- **Profit By Item**: Breakdown of profit by item

### Watchlists & Alerts

Create watchlists to monitor items for specific conditions:

1. Navigate to **Flipping → Watchlist**
2. Click **Add to Watchlist** (or use the button from flip results)
3. Select alert type:
   - **Price Below**: Alert when price drops below threshold
   - **Price Above**: Alert when price rises above threshold
   - **Margin Above**: Alert when profit margin exceeds threshold
4. Set your threshold value
5. Click **Add**

**Alert Notifications**: Alerts are evaluated every 5 minutes. When triggered, they appear in the **Alerts** section. Alerts have a 1-hour cooldown to prevent spam.

### Tips for Flipping

- **Start Small**: Begin with lower budgets to learn the market
- **Check Volume**: High volume items are easier to flip but may have lower margins
- **Monitor Trends**: Use watchlists to track items over time
- **Log Everything**: Accurate trade logging helps identify profitable patterns
- **Tax Awareness**: Remember GE tax affects your profit margins

## Gear Calculator

The Gear Calculator helps you optimize your equipment loadouts, calculate DPS, and plan your gear progression.

### Loadout Builder

Build and compare gear loadouts:

1. Navigate to **Gear → Loadout Builder**
2. Select items for each equipment slot
3. Set your combat stats (Attack, Strength, Defence, Ranged, Magic, Prayer)
4. Choose combat style (Melee, Ranged, Magic)
5. View calculated stats and DPS

### DPS Lab

Compare multiple loadouts side-by-side:

1. Navigate to **Gear → DPS Lab**
2. Build or select multiple loadouts
3. Configure combat settings:
   - Combat style
   - Attack type
   - Player stats
   - Target monster (optional)
4. View comparison results:
   - DPS for each loadout
   - Max hit
   - Accuracy
   - Attack speed
   - Marginal gains (DPS increase per upgrade)

**Use Cases**:
- Compare budget vs. expensive loadouts
- Evaluate upgrade paths
- Optimize for specific bosses

### Best-in-Slot (BiS) Calculator

Find the best gear for your budget and constraints:

1. Navigate to **Gear → Boss BiS** (or use the BiS calculator)
2. Select a boss (Vorkath, Zulrah, TOA, GWD)
3. Set your budget
4. Enter your combat stats
5. Apply constraints:
   - **Ironman Mode**: Filter out tradeable items
   - **Exclude Items**: List items to exclude
   - **Max Tick Manipulation**: Filter items requiring tick manipulation
6. View recommended loadout(s)

### Upgrade Path Recommendations

Get personalized upgrade suggestions:

1. Navigate to **Gear → Progression**
2. Select your combat style (Melee, Ranged, Magic)
3. Enter your current stats and budget
4. View prioritized upgrade recommendations:
   - Items sorted by DPS/GP ratio
   - DPS increase per upgrade
   - Cost and requirements

### Wiki Progression

Browse gear progression tiers from the OSRS Wiki:

1. Navigate to **Gear → Progression**
2. Select combat style
3. Browse tiers organized by game stage:
   - Early game
   - Mid game
   - Late game
4. View items with stats, requirements, and content tags

### Tips for Gear Optimization

- **Budget First**: Use BiS calculator to find best gear within your budget
- **DPS/GP Ratio**: Higher ratios indicate better value upgrades
- **Consider Requirements**: Check quest and achievement requirements
- **Boss-Specific**: Use boss BiS for optimal setups
- **Progression Path**: Follow upgrade path recommendations for efficient progression

## Slayer Tracker

The Slayer Tracker helps you manage slayer tasks, find optimal locations, and get combat advice.

### Task Helper

Browse tasks by slayer master:

1. Navigate to **Slayer → Task Advisor**
2. Select a slayer master (Duradel, Konar, Nieve, etc.)
3. Browse available tasks
4. Click **Get Advice** on any task to see:
   - Recommendation (DO/SKIP/BLOCK)
   - Reasoning based on your stats
   - XP rates
   - Profit rates
   - Requirements

### Monster Database

Search and filter all monsters:

1. Navigate to **Slayer → Monster Database**
2. Use search to find specific monsters
3. Filter by category:
   - Dragons
   - Demons
   - Undead
   - Kalphite
4. Sort by:
   - Combat level
   - Slayer XP
   - Name
5. Click **Get Advice** to see task-specific information

### Task Advice

Get personalized recommendations:

1. Click **Get Advice** on any task
2. Enter your stats:
   - Slayer level (1-99)
   - Combat level (3-126)
3. View recommendation:
   - **DO**: Good task for your level
   - **SKIP**: Consider skipping this task
   - **BLOCK**: Consider blocking this task
4. See detailed reasoning and alternatives

### Location Information

View detailed location data:

1. Click on a task to see location information
2. View available locations with:
   - Requirements (quests, favors, etc.)
   - Multi-combat vs single-combat
   - Cannon availability
   - Safespot availability
   - Pros and cons
   - Best use cases
3. See alternative monsters that count for the task
4. View strategy recommendations and optimal setups

### Tips for Slayer

- **Master Selection**: Choose masters appropriate for your level
- **Task Weight**: Consider task weights when planning blocks
- **Location Research**: Check location requirements before starting
- **Alternative Monsters**: Some tasks have easier alternatives
- **XP vs Profit**: Balance XP rates with profit potential

## Keyboard Shortcuts

- **R**: Refresh flip opportunities (Flipping page)
- **F**: Focus filter input (Flipping page)

More shortcuts may be added in future updates.

## FAQ

### General

**Q: Is my data stored on a server?**  
A: No, your user ID and preferences are stored locally in your browser. Trade and watchlist data is stored in the application database but associated with your user ID.

**Q: Can I use this on mobile?**  
A: The application is responsive and works on mobile devices, though desktop is recommended for the best experience.

**Q: How often are prices updated?**  
A: Prices are updated every 5 minutes from the OSRS Wiki API.

**Q: Are the calculations accurate?**  
A: Yes! The tool uses official game formulas and data from the OSRS Wiki. DPS calculations follow established formulas, and tax calculations match the in-game GE tax system.

### Flipping

**Q: Why don't I see any flip opportunities?**  
A: Make sure your filters aren't too restrictive. Try lowering the minimum ROI or increasing the max budget. Also ensure the database has price data (prices update every 5 minutes).

**Q: How accurate are the profit calculations?**  
A: Profit calculations account for GE tax (2% with 5M cap) and use current buy/sell prices from the OSRS Wiki API.

**Q: Can I track multiple accounts?**  
A: Currently, the tool uses a single user ID per browser. To track multiple accounts, you would need to use different browsers or clear localStorage between uses.

**Q: How do watchlist alerts work?**  
A: Alerts are evaluated every 5 minutes. When a condition is met, an alert is created. Alerts have a 1-hour cooldown to prevent spam.

### Gear

**Q: How accurate are DPS calculations?**  
A: DPS calculations use established formulas from the OSRS community. They account for accuracy, max hit, attack speed, and monster defence stats.

**Q: Can I save my loadouts?**  
A: Currently, loadouts are session-based. Future updates may include loadout saving.

**Q: What's the difference between BiS and upgrade path?**  
A: BiS finds the best gear for a specific budget and constraints. Upgrade path shows the optimal order to upgrade your gear over time.

**Q: Are ironman constraints accurate?**  
A: Ironman mode filters out tradeable items, but you should verify quest and achievement requirements yourself.

### Slayer

**Q: How accurate are the DO/SKIP/BLOCK recommendations?**  
A: Recommendations are based on XP rates, profit rates, and your combat/slayer levels. They're guidelines - your playstyle and preferences may differ.

**Q: Why don't all tasks have location data?**  
A: Location data is being added continuously. Currently, ~85% of Nieve tasks have complete location data.

**Q: Can I filter tasks by XP rate or profit?**  
A: Filtering by XP/profit is planned for a future update. Currently, you can search and sort tasks.

**Q: How do I know which master to use?**  
A: Choose masters appropriate for your combat and slayer level. Higher-level masters offer better XP and profit but require higher levels.

### Technical

**Q: What browsers are supported?**  
A: Modern browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled.

**Q: Why is the API rate limited?**  
A: Rate limiting protects the service and ensures fair usage. Default limit is 100 requests per minute per IP.

**Q: Can I use the API directly?**  
A: Yes! The API is documented at `/docs` when running locally. All endpoints are under `/api/v1/`.

**Q: Is the code open source?**  
A: Yes, the project is open source under the MIT License.

### Troubleshooting

**Q: The page won't load**  
A: Check your internet connection and ensure JavaScript is enabled. Try refreshing the page.

**Q: Prices aren't updating**  
A: Prices update every 5 minutes. If prices seem stale, click the refresh button or wait for the next update cycle.

**Q: I'm getting rate limit errors**  
A: You're making too many requests. Wait a minute and try again. The limit is 100 requests per minute.

**Q: My trades aren't showing up**  
A: Make sure you're using the same browser and haven't cleared localStorage. Trades are associated with your user ID.

**Q: DPS calculations seem wrong**  
A: Double-check your combat stats and loadout. Make sure you've selected the correct combat style and attack type.

## Getting Help

- **Issues**: Report bugs or request features on GitHub
- **API Documentation**: Visit `/docs` when running locally
- **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines

---

*Last Updated: 2026-01-28*
