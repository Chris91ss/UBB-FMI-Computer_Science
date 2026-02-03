using System;

namespace rt
{
    class RayTracer(Geometry[] geometries, Light[] lights)
    {
        private double ImageToViewPlane(int n, int imgSize, double viewPlaneSize)
        {
            return -n * viewPlaneSize / imgSize + viewPlaneSize / 2;
        }

        private Intersection FindFirstIntersection(Line ray, double minDist, double maxDist)
        {
            var intersection = Intersection.NONE;

            foreach (var geometry in geometries)
            {
                var intr = geometry.GetIntersection(ray, minDist, maxDist);

                if (!intr.Valid || !intr.Visible) continue;

                if (!intersection.Valid || !intersection.Visible)
                {
                    intersection = intr;
                }
                else if (intr.T < intersection.T)
                {
                    intersection = intr;
                }
            }

            return intersection;
        }

        // checking if anything blocks the path from the surface point to the light.
        private bool IsLit(Vector point, Light light)
        {
            // TODO: ADD CODE HERE
            // Create a line from the point to the light source
            var incidentLine = new Line(point, light.Position);

            // Use a small epsilon to avoid self-intersection.
            const double epsilon = 1e-10;

            // Calculate the distance to the light
            var lightDistance = (light.Position - point).Length();

            // Check for intersections with scene geometries
            foreach (var geometry in geometries)
            {
                // Skip CtScan geometry for shadow calculations
                if (geometry is CtScan)
                    continue;

                var intersection = geometry.GetIntersection(incidentLine, epsilon, lightDistance);

                // If there's a visible intersection, the point is in shadow
                if (intersection.Visible)
                    return false;
            }

            return true;
        }

        public void Render(Camera camera, int width, int height, string filename)
        {
            var background = new Color(0.2, 0.2, 0.2, 1.0);

            var image = new Image(width, height);

            // Calculate view plane vectors
            var viewParallel = (camera.Up ^ camera.Direction).Normalize();
            var viewDirection = camera.Direction * camera.ViewPlaneDistance;

            for (var i = 0; i < width; i++)
            { // loop through each pixel in the image
                for (var j = 0; j < height; j++)
                {
                    // TODO: ADD CODE HERE
                    // Calculate view plane coordinates (Convert pixel index -> view plane coordinate)
                    var viewPlaneX = ImageToViewPlane(i, width, camera.ViewPlaneWidth); // Convert x-pixel index to view plane x-coordinate
                    var viewPlaneY = ImageToViewPlane(j, height, camera.ViewPlaneHeight); // Convert y-pixel index to view plane y-coordinate

                    // Calculate ray direction, start at camera, pass through the view plane point.
                    var rayVector = camera.Position + viewDirection + viewParallel * viewPlaneX + camera.Up * viewPlaneY; // Compute point on the view plane
                    var ray = new Line(camera.Position, rayVector); // Create ray from camera through that point:

                    // Find first intersection (find the closest hit)
                    var intersection = FindFirstIntersection(ray, camera.FrontPlaneDistance, camera.BackPlaneDistance);

                    if (!intersection.Visible) // if no intersection, set the pixel to the background color
                    {
                        image.SetPixel(i, j, background);
                        continue;
                    }

                    // Calculate lighting (ambient, diffuse, specular)
                    var pixelColor = new Color(); // initialize the pixel color to black
                    var pointOnSurface = intersection.Position; // get the point on the surface
                    var eyeVector = (camera.Position - pointOnSurface).Normalize(); // direction from the point to the camera
                    var surfaceNormal = intersection.Normal; // normal vector of the surface at the intersection point

                    foreach (var light in lights) // loop through each light
                    {
                        // Ambient component (always added)
                        var ambientComponent = intersection.Material.Ambient * light.Ambient;

                        if (IsLit(pointOnSurface, light)) // If the point is lit:
                        {
                            // Calculate light direction and reflection
                            var lightDirection = (light.Position - pointOnSurface).Normalize();
                            var reflectionDirection = (surfaceNormal * (surfaceNormal * lightDirection) * 2 - lightDirection).Normalize();

                            // Calculate diffuse and specular factors
                            var diffuseFactor = surfaceNormal * lightDirection;
                            var specularFactor = eyeVector * reflectionDirection;

                            // Add diffuse component
                            if (diffuseFactor > 0)
                            {
                                // Diffuse: matte shading based on the angle between normal and light
                                pixelColor += intersection.Material.Diffuse * light.Diffuse * diffuseFactor;
                            }

                            // Add specular component
                            if (specularFactor > 0)
                            {
                                // Specular: shiny highlights based on the reflection direction
                                pixelColor += intersection.Material.Specular * light.Specular * Math.Pow(specularFactor, intersection.Material.Shininess);
                            }
                        }

                        // Add ambient component
                        pixelColor += ambientComponent;
                    }

                    // After all lights, set the pixel color.
                    image.SetPixel(i, j, pixelColor);
                }
            }

            // After all pixels, save the image.
            image.Store(filename);
        }
    }
}