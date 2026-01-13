# Memory Requirements for Big Data Generation

## Overview
This document estimates the memory requirements for generating big data datasets with `BIG_DATA_MODE = True`.

## Dataset Sizes
- **Population Registry**: 1,500,000 records
- **Applications**: 800,000 records
- **Total Records**: 2,300,000 records

## Memory Estimation Breakdown

### 1. In-Memory DataFrame Requirements

#### Population Registry DataFrame (1.5M records)
**Columns (12 total):**
- `sa_id_number`: string (13 chars) ≈ 13 bytes
- `first_name`: string (avg 10 chars) ≈ 10 bytes
- `last_name`: string (avg 12 chars) ≈ 12 bytes
- `date_of_birth`: string (10 chars) ≈ 10 bytes
- `gender`: string (4-6 chars) ≈ 6 bytes
- `citizenship_status`: string (20 chars) ≈ 20 bytes
- `province`: string (15 chars) ≈ 15 bytes
- `city`: string (15 chars) ≈ 15 bytes
- `street_address`: string (30 chars) ≈ 30 bytes
- `postal_code`: string (4-5 chars) ≈ 5 bytes
- `cell_number`: string (10-13 chars) ≈ 12 bytes
- `record_created_date`: string (10 chars) ≈ 10 bytes

**Per record average**: ~162 bytes
**Raw data**: 1,500,000 × 162 bytes = **243 MB**

**Pandas overhead** (index, metadata, object pointers): Typically 2-3x raw data
**Estimated in-memory size**: **500-750 MB**

#### Applications DataFrame (800K records)
**Columns (11 total):**
- `application_id`: string (10 chars) ≈ 10 bytes
- `sa_id_number`: string (13 chars) ≈ 13 bytes
- `application_type`: string (6-8 chars) ≈ 8 bytes
- `application_date`: string (10 chars) ≈ 10 bytes
- `application_status`: string (8-12 chars) ≈ 10 bytes
- `province`: string (15 chars) ≈ 15 bytes
- `dha_branch_name`: string (15 chars) ≈ 15 bytes
- `branch_code`: string (4 chars) ≈ 4 bytes
- `submission_channel`: string (10 chars) ≈ 10 bytes
- `processing_days`: integer (4 bytes) ≈ 4 bytes
- `last_updated_date`: string (10 chars) ≈ 10 bytes

**Per record average**: ~113 bytes
**Raw data**: 800,000 × 113 bytes = **90 MB**

**Pandas overhead**: 2-3x raw data
**Estimated in-memory size**: **200-300 MB**

### 2. Peak Memory During Generation

During data generation, both DataFrames exist simultaneously in memory:
- Population DataFrame: 500-750 MB
- Applications DataFrame: 200-300 MB
- Temporary lists/dictionaries: ~50-100 MB
- Python interpreter overhead: ~100-200 MB

**Total peak memory**: **850 MB - 1.35 GB**

### 3. File Size Estimates

#### CSV Files (compressed text)
- **Population Registry CSV**: ~250-300 MB
- **Applications CSV**: ~100-120 MB
- **Total CSV size**: ~350-420 MB

#### XLSX Files (compressed XML)
- **Population Registry XLSX**: ~200-250 MB (compressed format)
- **Applications XLSX**: ~80-100 MB (compressed format)
- **Total XLSX size**: ~280-350 MB

**Total disk space required**: **630-770 MB**

## Recommended System Requirements

### Minimum Requirements
- **RAM**: 2 GB available
- **Disk Space**: 1 GB free
- **CPU**: Any modern processor (generation is CPU-bound)

### Recommended Requirements
- **RAM**: 4 GB available (for comfortable operation)
- **Disk Space**: 2 GB free (for safety margin)
- **CPU**: Multi-core processor (faster generation)

### Optimal Requirements
- **RAM**: 8 GB+ available
- **Disk Space**: 5 GB free (for multiple runs)
- **CPU**: 4+ cores, 2.5+ GHz
- **Storage**: SSD (faster file I/O)

## Performance Estimates

### Generation Time (approximate)
- **Population Registry (1.5M records)**: 5-15 minutes
- **Applications (800K records)**: 3-10 minutes
- **Data quality injection**: 2-5 minutes
- **File saving (CSV + XLSX)**: 5-15 minutes

**Total estimated time**: **15-45 minutes** (depending on system)

### Factors Affecting Performance
- CPU speed and cores
- RAM speed
- Disk I/O speed (SSD vs HDD)
- System load (other running applications)

## Memory Optimization Tips

1. **Close other applications** before running big data generation
2. **Use SSD storage** for faster file writes
3. **Monitor memory usage** with Task Manager (Windows) or Activity Monitor (Mac)
4. **Run during off-peak hours** if system is shared
5. **Consider generating in batches** if memory is limited (modify script to process in chunks)

## Warning Signs of Insufficient Memory

- Script becomes very slow or freezes
- System starts swapping to disk (high disk activity)
- "Out of Memory" errors
- System becomes unresponsive

If you encounter these issues, reduce the dataset sizes or increase available RAM.

## Summary

| Component | Size |
|-----------|------|
| **Peak RAM Usage** | 850 MB - 1.35 GB |
| **Disk Space (CSV)** | 350-420 MB |
| **Disk Space (XLSX)** | 280-350 MB |
| **Total Disk Space** | 630-770 MB |
| **Recommended RAM** | 4 GB available |
| **Estimated Time** | 15-45 minutes |

