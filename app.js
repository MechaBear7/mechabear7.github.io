"use strict";
const chinesePage = document.documentElement.lang.toLowerCase().startsWith("zh");
const siteRoot = new URL(chinesePage ? "../" : "./", document.baseURI);
function mediaUrl(value) {
  if (typeof value !== "string" || !value.trim()) return null;
  try {
    const url = new URL(value, siteRoot);
    return ["https:", "http:"].includes(url.protocol) ? url.href : null;
  } catch { return null; }
}
async function loadProjectMedia() {
  try {
    const response = await fetch(new URL(chinesePage ? "assets/media.zh.json" : "assets/media.json", siteRoot), {cache: "no-cache"});
    if (!response.ok) return;
    const config = await response.json();
    document.querySelectorAll("[data-media-id]").forEach(frame => {
      const configured = config[frame.dataset.mediaId];
      const spec = frame.dataset.mediaDisplay === "preview"
        ? {type: "image", src: configured?.preview, alt: configured?.previewAlt || configured?.alt}
        : configured;
      if (!spec || !["video", "image"].includes(spec.type)) return;
      const src = mediaUrl(spec.src);
      if (!src) return;
      const placeholder = frame.querySelector(".media-placeholder");
      const media = document.createElement(spec.type === "video" ? "video" : "img");
      media.className = "project-media";
      let caption;
      function ready() {
        if (placeholder) placeholder.hidden = true;
        if (spec.caption && !caption) {
          caption = document.createElement("figcaption");
          caption.className = "media-caption";
          caption.textContent = spec.caption;
          frame.append(caption);
        }
      }
      if (spec.type === "video") {
        media.controls = true;
        media.muted = spec.muted === true;
        media.defaultMuted = spec.muted === true;
        media.playsInline = true;
        media.preload = "metadata";
        media.setAttribute("aria-label", spec.alt || "项目演示视频");
        const poster = mediaUrl(spec.poster);
        if (poster) media.poster = poster;
        media.addEventListener("loadedmetadata", ready, {once:true});
      } else {
        media.alt = spec.alt || "项目演示";
        media.loading = "lazy";
        media.addEventListener("load", ready, {once:true});
      }
      media.addEventListener("error", () => {
        media.remove();
        caption?.remove();
        if (placeholder) placeholder.hidden = false;
      }, {once:true});
      frame.append(media);
      media.src = src;
    });
  } catch (error) { console.warn("Project media configuration could not be loaded", error); }
}
loadProjectMedia();

// Keep a single playback session active across the project demonstrations.
document.addEventListener("play", event => {
  if (!(event.target instanceof HTMLVideoElement)) return;
  document.querySelectorAll("video").forEach(video => {
    if (video !== event.target && !video.paused) video.pause();
  });
}, true);

// Language changes keep the visitor on the same project section.
const languageSwitch = document.querySelector(".language-switch");
if (languageSwitch && location.hash) languageSwitch.hash = location.hash;
