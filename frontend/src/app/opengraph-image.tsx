import { ImageResponse } from "next/og";

export const alt = "Abdulla Chowdry - AI and Data Engineer";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "1200px",
          height: "630px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "68px",
          background:
            "linear-gradient(135deg, #090d12 0%, #101b20 60%, #071510 100%)",
          color: "#ffffff",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
          <div
            style={{
              width: "84px",
              height: "84px",
              borderRadius: "20px",
              background: "#102b24",
              border: "1px solid #246b50",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#34d399",
              fontSize: "62px",
              fontWeight: 800,
            }}
          >
            A
          </div>

          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ fontSize: "34px", fontWeight: 700 }}>
              Abdulla Chowdry
            </div>
            <div
              style={{
                color: "#34d399",
                fontSize: "17px",
                letterSpacing: "7px",
                marginTop: "8px",
              }}
            >
              AI + DATA ENGINEER
            </div>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <div
            style={{
              fontSize: "61px",
              fontWeight: 750,
              lineHeight: 1.15,
              maxWidth: "1000px",
            }}
          >
            Engineering intelligent systems at scale.
          </div>

          <div
            style={{
              marginTop: "25px",
              fontSize: "23px",
              color: "#9ca3af",
            }}
          >
            AI Engineering · Data Platforms · Cloud Architecture
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            borderTop: "1px solid #26343a",
            paddingTop: "24px",
            color: "#34d399",
            fontSize: "19px",
          }}
        >
          <span>5+ Years Experience</span>
          <span>Production AI Systems</span>
          <span>abdullachowdry.com</span>
        </div>
      </div>
    ),
    { ...size }
  );
}
