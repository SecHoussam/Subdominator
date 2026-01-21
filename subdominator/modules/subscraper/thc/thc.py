import httpx
from subdominator.modules.logger.logger import logger

thcs = []

async def thc(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    global thcs

    try:
        if args.include_resources and "thc" not in args.include_resources and not args.all:
            return thcs
        
        if args.exclude_resources and "thc" in args.exclude_resources:
            return thcs

        url = "https://ip.thc.org/api/v1/lookup/subdomains"

        payload = {
            "domain": domain,
            "page_state": "",
            "limit": 100
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = await session.post(
            url,
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            logger.error(f"[THC] HTTP {response.status_code} for {domain}")
            return thcs

        data = response.json()

        # ---- Parse result safely ----
        results = data.get("results", [])
        for item in results:
            sub = item.get("subdomain")
            if sub:
                thcs.append(sub)

        logger.success(f"[THC] Found {len(thcs)} subdomains for {domain}")
        return thcs

    except httpx.RequestError as e:
        logger.error(f"[THC] Request error: {e}")

    except Exception as e:
        logger.error(f"[THC] Unexpected error: {e}")

    return thcs
