# 金葡进化树构建
## 数据
7株外部数据,4株SA开头XT1突变,4株JP开头Hq1突变;
## 结果
### calling SNP
#### snippy
```bash
for i  in fasta/*;do j=$(echo $i|awk -F [/.] '{print $2}');snippy --outdir snippy/$j --ref ref_fasta/GCF_000013425.1_ASM1342v1_genomic.fna --ctgs $i;done
```
- 7株(抗性菌)没有SNP差异
![quicker_5b06b1f9-d0f6-4fc9-862b-6512462c1c0b.png](https://i.loli.net/2020/05/21/51xze3dywXLt7u2.png)
#### parsnp

```bash
parsnp -r ref_fasta/GCF_000013425.1_ASM1342v1_genomic.fna -d fasta -p 8 -o SNP_parsnp
```

- 7株(抗性菌)被排除
![quicker_8455bbfd-2ec6-43a1-8344-3379a2f4b5e9.png](https://i.loli.net/2020/05/21/eUNmZaWF6criIxV.png)

- mlst菌株鉴定

  > 稀有菌株,mlst没有结果.

![quicker_f42f8ba2-36a7-4d03-ab9e-014c9bdd0219.png](https://i.loli.net/2020/05/21/LO7m4KEeAsab9hP.png)

### 生成aln文件

``` bash
snippy-core -r ../ref_fasta/GCF_000013425.1_ASM1342v1_genomic.fna --prefix core-snps {J,S}*l
```

### raxml建树

```bash
raxmlHPC -f a -p 12345 -x 12345 -#100 -s core-snps.aln  -m GTRGAMMAI -n core-snps
```



