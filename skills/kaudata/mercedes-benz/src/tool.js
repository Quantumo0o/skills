/**
 * Finds Mercedes-Benz USA dealers in a specific state or near a zip code.
 */
async function getMbusaDealers(zipCode, start = 0, count = 10, filter = "mbdealer") {
    const baseUrl = "https://nafta-service.mbusa.com/api/dlrsrv/v1/us/search";
    
    const apiUrl = new URL(baseUrl);
    apiUrl.searchParams.append("zip", zipCode);
    apiUrl.searchParams.append("start", start);
    apiUrl.searchParams.append("count", count);
    apiUrl.searchParams.append("filter", filter);

    const headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    };

    try {
        const response = await fetch(apiUrl, { headers });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        const dealers = (data.results || []).map(dealer => {
            const primaryAddress = dealer.address && dealer.address.length > 0 ? dealer.address[0] : {};
            const location = primaryAddress.location || {};

            const contacts = dealer.contact || [];
            const mainPhone = contacts.find(c => c.type === "phone");
            const servicePhone = contacts.find(c => c.type === "servicePhone");

            const activities = dealer.activities || [];
            const serviceActivity = activities.find(a => a.name === "service");

            return {
                id: dealer.id,
                name: dealer.name,
                address: primaryAddress.line1,
                city: primaryAddress.city,
                state: primaryAddress.state,
                zip: primaryAddress.zip,
                distance: location.dist ? `${location.dist} ${location.distunit}` : "Unknown distance",
                mainPhone: mainPhone ? mainPhone.value : "N/A",
                servicePhone: servicePhone ? servicePhone.value : "N/A",
                websiteUrl: dealer.url || "N/A",
                serviceUrl: serviceActivity ? serviceActivity.url : "N/A"
            };
        });

        return JSON.stringify({ 
            status: "success", 
            totalFound: data.totalCount || dealers.length,
            dealers: dealers 
        });

    } catch (error) {
        return JSON.stringify({ status: "error", message: error.message });
    }
}

/**
 * Finds Mercedes-Benz USA new vehicle inventory near a specific zip code.
 */
async function getMbusaInventory(params) {
    const baseUrl = "https://nafta-service.mbusa.com/api/inv/v1/en_us/new/vehicles/search";
    const apiUrl = new URL(baseUrl);

    // Required parameter
    if (params.zip) apiUrl.searchParams.append("zip", params.zip);
    
    // Pagination and base filters
    apiUrl.searchParams.append("start", params.start || 0);
    apiUrl.searchParams.append("count", params.count || 12);
    apiUrl.searchParams.append("withFilters", "true"); 

    // Directly mapped parameters
    if (params.dealerId) apiUrl.searchParams.append("dealerId", params.dealerId);
    if (params.distance) apiUrl.searchParams.append("distance", params.distance);
    if (params.model) apiUrl.searchParams.append("model", params.model);
    if (params.classId) apiUrl.searchParams.append("class", params.classId);
    if (params.bodyStyle) apiUrl.searchParams.append("bodyStyle", params.bodyStyle);
    if (params.brand) apiUrl.searchParams.append("brand", params.brand);
    if (params.exteriorColor) apiUrl.searchParams.append("exteriorColor", params.exteriorColor);
    if (params.interiorColor) apiUrl.searchParams.append("interiorColor", params.interiorColor);
    if (params.year) apiUrl.searchParams.append("year", params.year);
    if (params.highwayFuelEconomy) apiUrl.searchParams.append("highwayFuelEconomy", params.highwayFuelEconomy);
    if (params.passengerCapacity) apiUrl.searchParams.append("passengerCapacity", params.passengerCapacity);
    if (params.fuelType) apiUrl.searchParams.append("fuelType", params.fuelType);

    // Dynamic Price Formatting (MIN_MAX)
    if (params.minPrice !== undefined || params.maxPrice !== undefined) {
        const min = params.minPrice !== undefined ? params.minPrice : 0;
        const max = params.maxPrice !== undefined ? params.maxPrice : 999000;
        apiUrl.searchParams.append("price", `${min}_${max}`);
    }

    const headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    };

    try {
        const response = await fetch(apiUrl, { headers });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const records = data?.result?.pagedVehicles?.records || [];

        const vehicles = records.map(car => {
            const distance = car.dealer?.address?.[0]?.location?.dist 
                ? `${car.dealer.address[0].location.dist} miles` 
                : "Unknown distance";

            // Extract actionable URLs for the LLM
            const serviceActivity = car.dealer?.activities?.find(a => a.name === "service");
            const imageUrl = car.images?.[0] || car.exteriorBaseImage?.desktop?.url || "N/A";
            const dealerUrl = car.dealer?.url || "N/A";
            const serviceUrl = serviceActivity ? serviceActivity.url : "N/A";

            return {
                vin: car.vin,
                stockId: car.stockId || car.vehicleAttributes?.stockId || "N/A",
                year: car.year,
                modelName: car.modelName,
                msrp: car.msrp,
                engine: car.engine,
                exteriorColor: car.paint?.name || car.exteriorMetaColor,
                interiorColor: car.upholstery?.name || car.interiorMetaColor,
                dealerName: car.dealer?.name || "Unknown Dealer",
                distance: distance,
                available: car.available,
                imageUrl: imageUrl,
                dealerWebsite: dealerUrl,
                scheduleServiceUrl: serviceUrl
            };
        });

        const totalCount = data?.result?.pagedVehicles?.paging?.totalCount || vehicles.length;

        return JSON.stringify({ 
            status: "success", 
            totalAvailable: totalCount,
            returnedCount: vehicles.length,
            inventory: vehicles 
        });

    } catch (error) {
        return JSON.stringify({ status: "error", message: error.message });
    }
}

module.exports = { getMbusaDealers, getMbusaInventory };