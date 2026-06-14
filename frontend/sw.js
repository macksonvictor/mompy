const CACHE_NAME = "mompy-v47";
const FILES = [
  "./",
  "./index.html",
  "./css/styles.css?v=47",
  "./js/app.js?v=47",
  "./manifest.webmanifest",
  "./assets/grade.png",
  "./assets/grade_entrada.png",
  "./assets/mompy_loading_base.png",
  "./assets/hepterakt_boot_monitor.png",
  "./assets/mompy_idle.ico",
  "./assets/mompy_idle.png",
  "./assets/mompy_talk_1.png",
  "./assets/mompy_talk_2.png",
  "./assets/mompy_happy.png",
  "./assets/mompy_sad.png",
  "./assets/mompy_shutdown.png",
  "./assets/desligando5.png",
  "./assets/desligando2.png",
  "./assets/desligando3.png",
  "./assets/desligando4.png",
  "./assets/audio/click.wav",
  "./assets/audio/run.wav",
  "./assets/audio/success.wav",
  "./assets/audio/error.wav",
  "./assets/audio/shutdown.wav",
  "./assets/audio/mompy_crt_ambient_loop_minimal.wav",
  "./assets/name_mompy.png",
  "./assets/hepterakt_boot_logo_green.png",
  "./assets/settings.svg",
  "./assets/square-arrow-up-left.svg",
  "./assets/square-arrow-down-right.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(FILES)));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key)),
        ),
      ),
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request)),
  );
});
