# Udemie releases

Build runners for the [Udemie](https://udemie.study) desktop app.

This repository holds **only CI workflows**. The application source is private: each build
fetches it with a read-only deploy key, builds the Linux (`.deb`, Snap) and Windows packages,
and publishes them. Builds are started by hand by the maintainer; nothing here runs on pushes or
pull requests.

Download Udemie from **https://udemie.study/downloads**.
