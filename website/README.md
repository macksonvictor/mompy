# Mompy website

Official static website for `mompy.co`.

## Local preview

```powershell
cd website
python -m http.server 8780
```

Open:

```txt
http://127.0.0.1:8780
```

## Vercel setup

Use this folder as the Vercel project root:

```txt
website
```

No build command is required. The site is static HTML, CSS, and JavaScript.

## Domain notes

Domain: `mompy.co`

Recommended flow:

1. Create or link the Vercel project using `website` as the root directory.
2. Add `mompy.co` and `www.mompy.co` in Vercel Domains.
3. In Cloudflare DNS, point the domain records to Vercel according to the values shown by Vercel.
4. Keep SSL/TLS mode in Cloudflare compatible with Vercel, usually Full.
