using System;
using System.IO;
using System.Text.RegularExpressions;

namespace rt;

public class CtScan: Geometry
{
    private readonly Vector _position;
    private readonly double _scale;
    private readonly ColorMap _colorMap;
    private readonly byte[] _data;

    private readonly int[] _resolution = new int[3];
    private readonly double[] _thickness = new double[3];
    private readonly Vector _v0;
    private readonly Vector _v1;

    public CtScan(string datFile, string rawFile, Vector position, double scale, ColorMap colorMap) : base(Color.NONE)
    {
        _position = position;
        _scale = scale;
        _colorMap = colorMap;

        var lines = File.ReadLines(datFile);
        foreach (var line in lines)
        {
            var kv = Regex.Replace(line, "[:\\t ]+", ":").Split(":");
            if (kv[0] == "Resolution")
            {
                _resolution[0] = Convert.ToInt32(kv[1]);
                _resolution[1] = Convert.ToInt32(kv[2]);
                _resolution[2] = Convert.ToInt32(kv[3]);
            } else if (kv[0] == "SliceThickness")
            {
                _thickness[0] = Convert.ToDouble(kv[1]);
                _thickness[1] = Convert.ToDouble(kv[2]);
                _thickness[2] = Convert.ToDouble(kv[3]);
            }
        }

        _v0 = position;
        _v1 = position + new Vector(_resolution[0]*_thickness[0]*scale, _resolution[1]*_thickness[1]*scale, _resolution[2]*_thickness[2]*scale);

        var len = _resolution[0] * _resolution[1] * _resolution[2];
        _data = new byte[len];
        using FileStream f = new FileStream(rawFile, FileMode.Open, FileAccess.Read);
        if (f.Read(_data, 0, len) != len)
        {
            throw new InvalidDataException($"Failed to read the {len}-byte raw data");
        }
    }
    
    private ushort Value(int x, int y, int z)
    {
        if (x < 0 || y < 0 || z < 0 || x >= _resolution[0] || y >= _resolution[1] || z >= _resolution[2])
        {
            return 0;
        }

        return _data[z * _resolution[1] * _resolution[0] + y * _resolution[0] + x];
    }

    public override Intersection GetIntersection(Line line, double minDist, double maxDist)
    {
        // TODO: ADD CODE HERE
        // Check if ray intersects with the bounding box, for each axis (x, y, z)
        var tMin = new double[3]; // where the ray enters the box on that axis
        var tMax = new double[3]; // where the ray exits the box on that axis
        
        for (int i = 0; i < 3; i++)
        {
            // Get the axis (x, y, or z) and the size of the volume along that axis.
            var axis = i == 0 ? _position.X : (i == 1 ? _position.Y : _position.Z);
            var size = i == 0 ? (_v1.X - _v0.X) : (i == 1 ? (_v1.Y - _v0.Y) : (_v1.Z - _v0.Z));
            // Get the origin and direction of the ray.
            var rayOrigin = i == 0 ? line.X0.X : (i == 1 ? line.X0.Y : line.X0.Z);
            var rayDirection = i == 0 ? line.Dx.X : (i == 1 ? line.Dx.Y : line.Dx.Z);
            
            if (Math.Abs(rayDirection) < 1e-10) // if the ray is parallel to the axis, check if it's inside the bounding box
            {
                if (rayOrigin < axis || rayOrigin > axis + size)
                    return Intersection.NONE;
                // This axis imposes no restriction on t, so use infinite values for the interval.
                tMin[i] = double.NegativeInfinity;
                tMax[i] = double.PositiveInfinity;
            }
            else // otherwise, compute where the ray enters and exits the box along the axis
            { 
                var t1 = (axis - rayOrigin) / rayDirection;
                var t2 = (axis + size - rayOrigin) / rayDirection;
                tMin[i] = Math.Min(t1, t2);
                tMax[i] = Math.Max(t1, t2);
            }
        }
        
        // latest entry and earliest exit across all axes
        var tNear = Math.Max(Math.Max(tMin[0], tMin[1]), tMin[2]); // if you entered X early, you’re not inside the box until you also entered Y and Z
        var tFar = Math.Min(Math.Min(tMax[0], tMax[1]), tMax[2]); // the moment you leave any axis range, you’ve left the box
        
        if (tNear > tFar || tFar < 0) // the ray misses the box
            return Intersection.NONE;

        // clamp the start and end to the min and max distances to respect camera limits   
        var start = Math.Max(tNear, minDist);
        var end = Math.Min(tFar, maxDist);
        
        if (start > end) // the ray misses the box
            return Intersection.NONE;
        
        // Volume rendering
        var stepSize = _scale; // distance between samples
        var firstIntersection = 0.0; // the first intersection with the volume
        var normal = new Vector(); 
        var globalColor = new Color(); // the accumulated color of the volume
        var lastAlpha = 1.0; // how much transparency remains (how much light can still pass)
        var passedFirst = false; // whether we found the first visible voxel
        
        for (var t = start; t <= end; t += stepSize) // loop through each sample
        {
            var point = line.CoordinateToPosition(t); // where in space am I when Ive walked t meters along the ray
            var pointColor = GetColor(point);
            
            if (pointColor.Alpha == 0) continue; // if the sample is transparent, skip it
            
            if (!passedFirst)
            {
                firstIntersection = t;
                normal = GetNormal(point);
                passedFirst = true;
            }
            
            globalColor += pointColor * pointColor.Alpha * lastAlpha; // blend
            lastAlpha *= (1 - pointColor.Alpha); // update remaining transparency
            
            if (lastAlpha < 1e-10) break;
        }
        
        if (!passedFirst)
        return Intersection.NONE;
            
        return new Intersection(true, true, this, line, firstIntersection, normal, Material.FromColor(globalColor), globalColor);
    }
    
    private int[] GetIndexes(Vector v)
    {
        return new []{
            (int)Math.Floor((v.X - _position.X) / _thickness[0] / _scale), 
            (int)Math.Floor((v.Y - _position.Y) / _thickness[1] / _scale),
            (int)Math.Floor((v.Z - _position.Z) / _thickness[2] / _scale)};
    }
    private Color GetColor(Vector v)
    {
        int[] idx = GetIndexes(v);

        ushort value = Value(idx[0], idx[1], idx[2]);
        return _colorMap.GetColor(value);
    }

    private Vector GetNormal(Vector v)
    {
        int[] idx = GetIndexes(v);
        double x0 = Value(idx[0] - 1, idx[1], idx[2]);
        double x1 = Value(idx[0] + 1, idx[1], idx[2]);
        double y0 = Value(idx[0], idx[1] - 1, idx[2]);
        double y1 = Value(idx[0], idx[1] + 1, idx[2]);
        double z0 = Value(idx[0], idx[1], idx[2] - 1);
        double z1 = Value(idx[0], idx[1], idx[2] + 1);

        return new Vector(x1 - x0, y1 - y0, z1 - z0).Normalize();
    }
}