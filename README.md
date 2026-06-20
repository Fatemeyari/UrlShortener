<h1>URL Shortener & Analytics Service</h1>

<p>A backend service for shortening URLs, managing user authentication, and tracking link usage analytics.</p>

<h2>Overview</h2>

<p>This project is a URL shortening system that allows users to convert long URLs into short links. It also includes an authentication system and tracks basic analytics for each URL visit, such as browser type and access time.
</p>
<h2>Features</h2>

<h3>Authentication</h3>

* User Registration
* User Login
* User Logout
* Password Reset

<h3>URL Shortening</h3>

* Create short URLs from long links
* Redirect short URLs to original URLs

<h3>Analytics</h3>

* Track URL visits
* Store browser information
* Store access timestamp

<h2>Database</h2>

<p>The project uses SQLite for data storage.</p>

<a href="https://github.com/Fatemeyari/UrlShortener/blob/main/docs/Untitled%20Diagram.drawio.png">
  <img src="docks/Untitled%20Diagram.drawio.png" alt="Database Diagram" width="900">
</a>


<h2>Technology Stack</h2>

* Python
* Django / FastAPI (or your framework)
* SQLite

<h2>How it works</h2>

1. User submits a long URL
2. System generates a unique short URL
3. Data is stored in SQLite database
4. When short URL is visited, user is redirected to original URL
5. Each visit is logged for analytics

<h2>License</h2>

<p>This project is intended for educational purposes. Feel free to fork it and enhance its features.</p>
