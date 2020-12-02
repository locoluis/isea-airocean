# isea-airocean
A map in the style of Buckminster Fuller’s Airocean World Map, using Snyder's equal-area projection

This Python code requires the pyproj package, which includes an implementation of [Snyder's equal-area projection](https://proj.org/operations/projections/isea.html).

I chose specific parameters for the projection's center and azimuth, in order to generate a map that can be rearranged like Fuller's. After doing so, the code determines the triangle or polygon where the chosen point is located, and then applies the required translations and rotations.

As there's no inverse implementation of the ISEA projection, there's no inverse of this transformation.
