use std::io::{self, Read, Write};

// 블러 뒤의 실제 8/4비트 전송 패킷. 개인 경로나 라벨은 패킷에 넣지 않습니다.
fn execute(args: &[String], input: &[u8]) -> Result<Vec<u8>, String> {
    if args.len() == 3 && args[0] == "feature-encode" {
        let kind = match args[1].as_str() { "f32" => 1, "f16" => 2, "i8" => 3, _ => return Err("특징 dtype 오류".into()) };
        let n: u32 = args[2].parse().map_err(|_| "특징 원소 수 오류")?;
        validate_feature(kind, n, input)?;
        let mut out = b"FTR1".to_vec();
        out.push(kind);
        out.extend(n.to_le_bytes());
        out.extend(input);
        Ok(out)
    } else if args.len() == 1 && args[0] == "feature-decode" {
        if input.len() < 9 || &input[..4] != b"FTR1" { return Err("특징 패킷 머리글 오류".into()); }
        let n = u32::from_le_bytes(input[5..9].try_into().map_err(|_| "원소 수 오류")?);
        validate_feature(input[4], n, &input[9..])?;
        Ok(input[9..].to_vec())
    } else if args.len() == 4 && args[0] == "encode" {
        let w: u16 = args[1].parse().map_err(|_| "잘못된 너비")?;
        let h: u16 = args[2].parse().map_err(|_| "잘못된 높이")?;
        let bits: u8 = args[3].parse().map_err(|_| "잘못된 비트수")?;
        if w == 0 || h == 0 || w > 512 || h > 512 || ![4, 8].contains(&bits) {
            return Err("지원하지 않는 크기/비트수".into());
        }
        let n = usize::from(w) * usize::from(h);
        if input.len() != n { return Err("픽셀 바이트 길이 불일치".into()); }
        let mut out = b"CTB1".to_vec();
        out.extend(w.to_le_bytes()); out.extend(h.to_le_bytes()); out.push(bits);
        if bits == 8 { out.extend(input); }
        else {
            for pair in input.chunks(2) {
                let high = ((u16::from(pair[0]) * 15 + 127) / 255) as u8;
                let low = if pair.len() == 2 { ((u16::from(pair[1]) * 15 + 127) / 255) as u8 } else { 0 };
                out.push(high << 4 | low);
            }
        }
        Ok(out)
    } else if args.len() == 1 && args[0] == "decode" {
        if input.len() < 9 || &input[..4] != b"CTB1" { return Err("패킷 머리글 오류".into()); }
        let w = u16::from_le_bytes([input[4], input[5]]);
        let h = u16::from_le_bytes([input[6], input[7]]);
        let bits = input[8];
        if w == 0 || h == 0 || w > 512 || h > 512 || ![4, 8].contains(&bits) { return Err("패킷 크기/비트수 오류".into()); }
        let n = usize::from(w) * usize::from(h);
        let expected = if bits == 8 { n } else { n.div_ceil(2) };
        if input.len() != 9 + expected { return Err("패킷 길이 오류".into()); }
        if bits == 8 { return Ok(input[9..].to_vec()); }
        if n % 2 == 1 && input[input.len()-1] & 15 != 0 { return Err("패킷 패딩 오류".into()); }
        Ok((0..n).map(|i| { let b = input[9+i/2]; (if i%2 == 0 { b >> 4 } else { b & 15 }) * 17 }).collect())
    } else { Err("사용법: encode 너비 높이 4|8 / decode / feature-encode f32|f16|i8 원소수 / feature-decode".into()) }
}

// shape와 INT8 scale은 Python의 전송 메타데이터에도 담고 실제 바이트 비용에 포함합니다.
fn validate_feature(kind: u8, n: u32, payload: &[u8]) -> Result<(), String> {
    if n == 0 || n > 32_000_000 { return Err("특징 원소 수 범위 오류".into()); }
    let width = match kind { 1 => 4, 2 => 2, 3 => 1, _ => return Err("특징 dtype 오류".into()) };
    if payload.len() != n as usize * width { return Err("특징 바이트 길이 불일치".into()); }
    if kind == 1 && payload.chunks_exact(4).any(|c| !f32::from_le_bytes(c.try_into().unwrap()).is_finite()) {
        return Err("특징 FP32 비유한값".into());
    }
    if kind == 2 && payload.chunks_exact(2).any(|c| u16::from_le_bytes([c[0],c[1]]) & 0x7c00 == 0x7c00) {
        return Err("특징 FP16 비유한값".into());
    }
    Ok(())
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut input = Vec::new();
    let feature = args.first().is_some_and(|x| x.starts_with("feature-"));
    let limit = if feature { 128_000_010 } else { 262154 };
    if let Err(e) = io::stdin().take(limit).read_to_end(&mut input) { eprintln!("입력 오류: {e}"); std::process::exit(2); }
    match execute(&args, &input) {
        Ok(out) => if let Err(e) = io::stdout().write_all(&out) { eprintln!("출력 오류: {e}"); std::process::exit(2); },
        Err(e) => { eprintln!("{e}"); std::process::exit(2); }
    }
}
