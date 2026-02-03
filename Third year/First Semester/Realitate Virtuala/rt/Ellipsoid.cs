using System;

namespace rt
{
    public class Ellipsoid : Geometry
    {
        private Vector Center { get; }
        private Vector SemiAxesLength { get; }
        private double Radius { get; }

        // Rotation of this ellipsoid (unit quaternion expected).
        public Quaternion Rotation { get; set; } = Quaternion.Identity;

        public Ellipsoid(Vector center, Vector semiAxesLength, double radius, Material material, Color color)
            : base(material, color)
        {
            Center = center;
            SemiAxesLength = semiAxesLength;
            Radius = radius;
        }

        public Ellipsoid(Vector center, Vector semiAxesLength, double radius, Color color)
            : base(color)
        {
            Center = center;
            SemiAxesLength = semiAxesLength;
            Radius = radius;
        }

        public Ellipsoid(Ellipsoid e)
            : this(new Vector(e.Center), new Vector(e.SemiAxesLength), e.Radius, new Material(e.Material), new Color(e.Color))
        {
        }

        // Allocation-free rotate (flipped cross order): This rotates a vector v by a quaternion q
        // t = 2 * (v × qv);  c = t × qv;  v' = v + w*t + c   (q must be unit)
        private static Vector RotateBy(in Quaternion q, in Vector v)
        {
            // t = 2 * (v × q.xyz)
            double tx = 2.0 * (v.Y * q.Z - v.Z * q.Y);
            double ty = 2.0 * (v.Z * q.X - v.X * q.Z);
            double tz = 2.0 * (v.X * q.Y - v.Y * q.X);

            // c = t × q.xyz
            double cx = ty * q.Z - tz * q.Y;
            double cy = tz * q.X - tx * q.Z;
            double cz = tx * q.Y - ty * q.X;

            return new Vector(
                v.X + q.W * tx + cx,
                v.Y + q.W * ty + cy,
                v.Z + q.W * tz + cz
            );
        }

        public override Intersection GetIntersection(Line line, double minDist, double maxDist)
        {
            // ---- local helper ----
            static Quaternion Conjugate(in Quaternion q) => new(q.W, -q.X, -q.Y, -q.Z);

            // 1) Move ray to object origin
            var o = line.X0 - Center;
            var d = line.Dx;

            // 2) Normalize rotation locally; identity fast-path
            var q = new Quaternion(Rotation.W, Rotation.X, Rotation.Y, Rotation.Z).Normalize();
            // Check if it's identity (no rotation).
            bool isIdentity =
                Math.Abs(q.W - 1.0) < 1e-12 &&
                Math.Abs(q.X) < 1e-12 &&
                Math.Abs(q.Y) < 1e-12 &&
                Math.Abs(q.Z) < 1e-12;

            // Conjugate the quaternion to get the inverse.
            var qInv = Conjugate(q);

            // 3) Transform ray to sphere space for M = T·R·S  (L^{-1} = S^{-1}·R^{-1})
            double ax = SemiAxesLength.X, ay = SemiAxesLength.Y, az = SemiAxesLength.Z;

            Vector s, dir; // sphere-space origin & direction
            if (isIdentity)
            {
                // If no rotation: just scale by the inverse semi-axes.
                // R = I ⇒ only S^{-1}
                s   = new Vector(o.X / ax, o.Y / ay, o.Z / az);
                dir = new Vector(d.X / ax, d.Y / ay, d.Z / az);
            }
            else
            {
                // If rotated: first undo the rotation, then scale.
                // First rotate by R^{-1}, then scale by S^{-1}
                var oRot = RotateBy(qInv, o);
                var dRot = RotateBy(qInv, d);
                s   = new Vector(oRot.X / ax, oRot.Y / ay, oRot.Z / az);
                dir = new Vector(dRot.X / ax, dRot.Y / ay, dRot.Z / az);
            }

            // 4) Quadratic on sphere: |s + t*dir|^2 = R^2
            // basically where the ray hits the sphere.
            double aQ = dir.Length2();
            if (aQ < 1e-15) return Intersection.NONE;

            double bQ = 2.0 * (s * dir);
            double cQ = s.Length2() - Radius * Radius;

            double disc = bQ * bQ - 4.0 * aQ * cQ;
            if (disc < -1e-12) return Intersection.NONE;
            if (disc < 0) disc = 0;

            double sqrtD = Math.Sqrt(disc);
            double inv2a = 0.5 / aQ;
            double t1 = (-bQ - sqrtD) * inv2a;
            double t2 = (-bQ + sqrtD) * inv2a;

            double t = double.PositiveInfinity;
            if (t1 >= minDist && t1 <= maxDist) t = t1;
            if (t2 >= minDist && t2 <= maxDist && t2 < t) t = t2;
            if (!double.IsFinite(t)) return Intersection.NONE;

            // 5) Normal: n_w ∝ L^{-T} n_s with L = R·S ⇒ L^{-T} = S^{-1} · R
            //  compute the surface normal (which way the surface faces) in world space.
            var pS = s + dir * t; // Compute the hit point in sphere space: => n_s = pS
            Vector nWorld;
            if (isIdentity)
            {
                nWorld = new Vector(pS.X / ax, pS.Y / ay, pS.Z / az);
            }
            else
            {
                var nRot = RotateBy(q, pS); // R
                nWorld = new Vector(nRot.X / ax, nRot.Y / ay, nRot.Z / az); // S^{-1}
            }
            // lighting needs the normal in world space.
            nWorld.Normalize();

            return new Intersection(true, true, this, line, t, nWorld, Material, Color);
        }
    }
}
